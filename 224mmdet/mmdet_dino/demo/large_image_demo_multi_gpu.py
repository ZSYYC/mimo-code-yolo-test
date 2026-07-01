"""
Multi-GPU version of large-image inference script.
Each GPU handles a split of image list independently.
tqdm progress bars are shown for each GPU.
"""

import os
import random
from argparse import ArgumentParser
from pathlib import Path
import torch
import multiprocessing as mp

import mmcv
import mmengine
import numpy as np
from mmengine.config import Config, ConfigDict
from mmengine.logging import print_log
from mmengine.structures import InstanceData
from tqdm import tqdm

from mmdet.apis import inference_detector, init_detector
from mmdet.structures import DetDataSample
from mmdet.registry import VISUALIZERS
from mmdet.utils.large_image import merge_results_by_nms, shift_predictions
from mmdet.utils.misc import get_file_list

# -------------------------------------------------------------
# pred2dict retains your original logic
# -------------------------------------------------------------
def pred2dict(filename, data_sample, pred_out_dir):
    img_path = os.path.basename(filename)
    img_path = os.path.splitext(img_path)[0]
    out_json_path = os.path.join(pred_out_dir, 'preds', img_path + '.json')

    os.makedirs(os.path.dirname(out_json_path), exist_ok=True)

    result = {}
    if 'pred_instances' in data_sample:
        pred_instances = data_sample.pred_instances.numpy()
        result = {
            'labels': pred_instances.labels.tolist(),
            'scores': pred_instances.scores.tolist()
        }
        if 'bboxes' in pred_instances:
            result['bboxes'] = pred_instances.bboxes.tolist()

    mmengine.dump(result, out_json_path)


# -------------------------------------------------------------
# filter_instances retains your original filtering logic
# -------------------------------------------------------------
def filter_instances(
        data_sample,
        min_area=1250,
        max_area=20000,
        min_ratio=0.4,
        max_ratio=2.5,
        min_w=40,
        max_w=180,
        min_h=50,
        max_h=180):

    if 'pred_instances' not in data_sample:
        return data_sample

    pred_instances = data_sample.pred_instances
    if len(pred_instances) == 0:
        return data_sample

    bboxes = pred_instances.bboxes
    widths = bboxes[:, 2] - bboxes[:, 0]
    heights = bboxes[:, 3] - bboxes[:, 1]
    heights_safe = torch.clamp(heights, min=1)
    areas = widths * heights

    area_mask = (areas >= min_area) & (areas <= max_area)
    size_mask = ((widths >= min_w) & (widths <= max_w) &
                 (heights >= min_h) & (heights <= max_h))
    ratios = widths / heights_safe
    ratio_mask = (ratios >= min_ratio) & (ratios <= max_ratio)

    final_mask = area_mask & size_mask & ratio_mask

    if not final_mask.any():
        filtered_instances = InstanceData(
            bboxes=bboxes.new_empty((0, 4)),
            scores=pred_instances.scores.new_empty((0,)),
            labels=pred_instances.labels.new_empty((0,))
        )
    else:
        filtered_instances = InstanceData(
            bboxes=pred_instances.bboxes[final_mask],
            scores=pred_instances.scores[final_mask],
            labels=pred_instances.labels[final_mask]
        )

    filtered_sample = data_sample.clone()
    filtered_sample.pred_instances = filtered_instances
    return filtered_sample


# -------------------------------------------------------------
# Per-GPU inference worker
# -------------------------------------------------------------
def gpu_worker(gpu_id, files, args):
    # ---- 关键：每个进程只暴露一个 GPU ----
    # os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    # torch.cuda.set_device(0)  # 在该进程视角中，只有一个GPU，就是0号

    # ---- load config ----
    config = Config.fromfile(args.config)
    if 'init_cfg' in config.model.backbone:
        config.model.backbone.init_cfg = None

    device = "cuda"  # 进程视角下只有一个GPU
    print("--------------gpu_id", gpu_id)
    model = init_detector(config, args.checkpoint, device=f'cuda:{gpu_id}', cfg_options={})

    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta

    from sahi.slicing import slice_image

    progress = tqdm(files, desc=f"GPU {gpu_id}", ncols=120)

    for file in progress:
        img = mmcv.imread(file)
        height, width = img.shape[:2]

        sliced_image_object = slice_image(
            img,
            slice_height=args.patch_size,
            slice_width=args.patch_size,
            auto_slice_resolution=False,
            overlap_height_ratio=args.patch_overlap_ratio,
            overlap_width_ratio=args.patch_overlap_ratio,
        )

        slice_results = []
        start = 0
        while start < len(sliced_image_object):
            end = min(start + args.batch_size, len(sliced_image_object))
            images = [sliced_image_object.images[i] for i in range(start, end)]
            slice_results.extend(inference_detector(model, images, text_prompt='insect'))
            start = end


        # merging
        image_result = merge_results_by_nms(
            slice_results,
            sliced_image_object.starting_pixels,
            src_image_shape=(height, width),
            nms_cfg={
                'type': args.merge_nms_type,
                'iou_threshold': args.merge_iou_thr
            }
        )

        # filtering
        filtered_result = filter_instances(
            image_result,
            min_area=args.min_area,
            max_area=args.max_area,
            min_ratio=0.4,
            max_ratio=2.5,
            min_w=40,
            max_w=180,
            min_h=50,
            max_h=180
        )

        # save json
        pred2dict(file, filtered_result, args.out_dir)


# -------------------------------------------------------------
# Argument parser
# -------------------------------------------------------------
def parse_args():
    parser = ArgumentParser(description='Multi-GPU Large Image Inference')

    parser.add_argument('img', help='Image file or directory')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument('--out-dir', default='./output', help='Output path')
    parser.add_argument('--device', default='cuda', help='Unused (for compatibility)')
    parser.add_argument('--patch-size', type=int, default=640)
    parser.add_argument('--patch-overlap-ratio', type=float, default=0.1)
    parser.add_argument('--merge-iou-thr', type=float, default=0.25)
    parser.add_argument('--merge-nms-type', type=str, default='nms')
    parser.add_argument('--batch-size', type=int, default=8)
    parser.add_argument('--min-area', type=float, default=1250)
    parser.add_argument('--max-area', type=float, default=20000)

    return parser.parse_args()


# -------------------------------------------------------------
# Split list helper
# -------------------------------------------------------------
def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]


# -------------------------------------------------------------
# Main: Multi-GPU Dispatcher
# -------------------------------------------------------------
def main():

    args = parse_args()

    files, src_type = get_file_list(args.img)
    print(f"Found {len(files)} images.")

    num_gpus = torch.cuda.device_count()
    print(f"Detected {num_gpus} GPUs.")

    os.makedirs(os.path.join(args.out_dir, 'preds'), exist_ok=True)

    file_splits = split_list(files, num_gpus)

    procs = []
    for gpu_id in range(num_gpus):
        p = mp.Process(target=gpu_worker, args=(gpu_id, file_splits[gpu_id], args))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    print("All GPUs finished inference.")


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    main()