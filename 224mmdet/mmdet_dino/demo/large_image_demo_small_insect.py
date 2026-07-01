# Copyright (c) OpenMMLab. All rights reserved.
"""Perform MMDET inference on large images (as satellite imagery) as:

```shell
wget -P checkpoint https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r101_fpn_2x_coco/faster_rcnn_r101_fpn_2x_coco_bbox_mAP-0.398_20200504_210455-1d2dac9c.pth # noqa: E501, E261.

python demo/large_image_demo.py \
    demo/large_image.jpg \
    configs/faster_rcnn/faster-rcnn_r101_fpn_2x_coco.py \
    checkpoint/faster_rcnn_r101_fpn_2x_coco_bbox_mAP-0.398_20200504_210455-1d2dac9c.pth
```
"""

import os
import random
from argparse import ArgumentParser
from pathlib import Path
import torch

import mmcv
import mmengine
import numpy as np
from mmengine.config import Config, ConfigDict
from mmengine.logging import print_log
from mmengine.utils import ProgressBar
from mmengine.structures import InstanceData

from mmdet.apis import inference_detector, init_detector

try:
    from sahi.slicing import slice_image
except ImportError:
    raise ImportError('Please run "pip install -U sahi" '
                      'to install sahi first for large image inference.')
from mmdet.structures import DetDataSample
from mmdet.registry import VISUALIZERS
from mmdet.utils.large_image import merge_results_by_nms, shift_predictions
from mmdet.utils.misc import get_file_list
def pred2dict(    filename,
                  data_sample: DetDataSample,
                  pred_out_dir: str = '',):
        img_path = os.path.basename(filename)
        img_path = os.path.splitext(img_path)[0]
        out_json_path = os.path.join(pred_out_dir, 'preds', img_path + '.json')
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
    """
    过滤规则：
    1. 面积过滤：min_area <= area <= max_area
    2. 长宽比过滤：min_ratio <= w/h <= max_ratio
    3. 宽高过滤：
        width  >= min_w and width  <= max_w
        height >= min_h and height <= max_h
    """
    if 'pred_instances' not in data_sample:
        return data_sample

    pred_instances = data_sample.pred_instances
    if len(pred_instances) == 0:
        return data_sample

    bboxes = pred_instances.bboxes
    if len(bboxes) == 0:
        return data_sample

    # ------------------------------------------------------
    # 计算宽、高、面积
    # ------------------------------------------------------
    widths = bboxes[:, 2] - bboxes[:, 0]
    heights = bboxes[:, 3] - bboxes[:, 1]

    # 避免除零
    heights_safe = torch.clamp(heights, min=1)

    areas = widths * heights

    # ------------------------------------------------------
    # 面积过滤
    # ------------------------------------------------------
    area_mask = (areas >= min_area) & (areas <= max_area)

    # ------------------------------------------------------
    # 宽高过滤
    # ------------------------------------------------------
    size_mask = (
        (widths >= min_w) & (widths <= max_w) &
        (heights >= min_h) & (heights <= max_h)
    )

    # ------------------------------------------------------
    # 长宽比过滤
    # ------------------------------------------------------
    ratios = widths / heights_safe
    ratio_mask = (ratios >= min_ratio) & (ratios <= max_ratio)

    # ------------------------------------------------------
    # 最终掩码 = 面积 + 长宽比 + 尺寸同时满足
    # ------------------------------------------------------
    final_mask = area_mask & size_mask & ratio_mask

    from mmengine.structures import InstanceData
    if not final_mask.any():
        filtered_instances = InstanceData()
        filtered_instances.bboxes = bboxes.new_empty((0, 4))
        filtered_instances.scores = pred_instances.scores.new_empty((0,))
        filtered_instances.labels = pred_instances.labels.new_empty((0,))
    else:
        filtered_instances = InstanceData()
        filtered_instances.bboxes = pred_instances.bboxes[final_mask]
        filtered_instances.scores = pred_instances.scores[final_mask]
        filtered_instances.labels = pred_instances.labels[final_mask]

    filtered_sample = data_sample.clone()
    filtered_sample.pred_instances = filtered_instances

    return filtered_sample


def parse_args():
    parser = ArgumentParser(
        description='Perform MMDET inference on large images.')
    parser.add_argument(
        'img', help='Image path, include image file, dir and URL.')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--out-dir', default='./output', help='Path to output file')
    parser.add_argument(
        '--device', default='cuda:1', help='Device used for inference')
    parser.add_argument(
        '--show', action='store_true', help='Show the detection results')
    parser.add_argument(
        '--tta',
        action='store_true',
        help='Whether to use test time augmentation')
    parser.add_argument(
        '--score-thr', type=float, default=0.3, help='Bbox score threshold')
    parser.add_argument(
        '--patch-size', type=int, default=640, help='The size of patches')
    parser.add_argument(
        '--patch-overlap-ratio',
        type=float,
        default=0.25,
        help='Ratio of overlap between two patches')
    parser.add_argument(
        '--merge-iou-thrmerge-iou-thr',
        type=float,
        default=0.25,
        help='IoU threshould for merging results')
    parser.add_argument(
        '--merge-nms-type',
        type=str,
        default='nms',
        help='NMS type for merging results')
    parser.add_argument(
        '--batch-size',
        type=int,
        default=1,
        help='Batch size, must greater than or equal to 1')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Export debug results before merging')
    parser.add_argument(
        '--save-patch',
        action='store_true',
        help='Save the results of each patch. '
        'The `--debug` must be enabled.')
    parser.add_argument(
        '--min-area',
        type=float,
        default=1250,
        help='Minimum bounding box area threshold')
    parser.add_argument(
        '--max-area',
        type=float,
        default=20000,
        help='Maximum bounding box area threshold')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    config = args.config

    if isinstance(config, (str, Path)):
        config = Config.fromfile(config)
    elif not isinstance(config, Config):
        raise TypeError('config must be a filename or Config object, '
                        f'but got {type(config)}')
    if 'init_cfg' in config.model.backbone:
        config.model.backbone.init_cfg = None

    if args.tta:
        assert 'tta_model' in config, 'Cannot find ``tta_model`` in config.' \
                                      " Can't use tta !"
        assert 'tta_pipeline' in config, 'Cannot find ``tta_pipeline`` ' \
                                         "in config. Can't use tta !"
        config.model = ConfigDict(**config.tta_model, module=config.model)
        test_data_cfg = config.test_dataloader.dataset
        while 'dataset' in test_data_cfg:
            test_data_cfg = test_data_cfg['dataset']

        test_data_cfg.pipeline = config.tta_pipeline

    # TODO: TTA mode will error if cfg_options is not set.
    #  This is an mmdet issue and needs to be fixed later.
    # build the model from a config file and a checkpoint file
    model = init_detector(
        config, args.checkpoint, device=args.device, cfg_options={})

    if not os.path.exists(args.out_dir) and not args.show:
        os.mkdir(args.out_dir)

    # init visualizer
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.dataset_meta = model.dataset_meta

    # get file list
    files, source_type = get_file_list(args.img)

    # start detector inference
    print(f'Performing inference on {len(files)} images.... '
          'This may take a while.')
    progress_bar = ProgressBar(len(files))
    # count = 0
    for file in files:
        # if count ==5:
        #     break
        # else:
        #     count = count + 1

        # read image
        img = mmcv.imread(file)

        # arrange slices
        height, width = img.shape[:2]
        sliced_image_object = slice_image(
            img,
            slice_height=args.patch_size,
            slice_width=args.patch_size,
            auto_slice_resolution=False,
            overlap_height_ratio=args.patch_overlap_ratio,
            overlap_width_ratio=args.patch_overlap_ratio,
        )
        # perform sliced inference
        slice_results = []
        start = 0
        while True:
            # prepare batch slices
            end = min(start + args.batch_size, len(sliced_image_object))
            images = []
            for sliced_image in sliced_image_object.images[start:end]:
                images.append(sliced_image)

            # forward the model
            slice_results.extend(inference_detector(model, images,text_prompt='insect'))

            if end >= len(sliced_image_object):
                break
            start += args.batch_size

        if source_type['is_dir']:
            filename = os.path.relpath(file, args.img).replace('/', '_')
        else:
            filename = os.path.basename(file)

        img = mmcv.imconvert(img, 'bgr', 'rgb')
        out_file = None if args.show else os.path.join(args.out_dir, filename)

        # export debug images
        if args.debug:
            # export sliced image results
            name, suffix = os.path.splitext(filename)

            shifted_instances = shift_predictions(
                slice_results,
                sliced_image_object.starting_pixels,
                src_image_shape=(height, width))
            merged_result = slice_results[0].clone()
            merged_result.pred_instances = shifted_instances

            debug_file_name = name + '_debug' + suffix
            debug_out_file = None if args.show else os.path.join(
                args.out_dir, debug_file_name)
            visualizer.set_image(img.copy())

            debug_grids = []
            for starting_point in sliced_image_object.starting_pixels:
                start_point_x = starting_point[0]
                start_point_y = starting_point[1]
                end_point_x = start_point_x + args.patch_size
                end_point_y = start_point_y + args.patch_size
                debug_grids.append(
                    [start_point_x, start_point_y, end_point_x, end_point_y])
            debug_grids = np.array(debug_grids)
            debug_grids[:, 0::2] = np.clip(debug_grids[:, 0::2], 1,
                                           img.shape[1] - 1)
            debug_grids[:, 1::2] = np.clip(debug_grids[:, 1::2], 1,
                                           img.shape[0] - 1)

            palette = np.random.randint(0, 256, size=(len(debug_grids), 3))
            palette = [tuple(c) for c in palette]
            line_styles = random.choices(['-', '-.', ':'], k=len(debug_grids))
            visualizer.draw_bboxes(
                debug_grids,
                edge_colors=palette,
                alpha=1,
                line_styles=line_styles)
            visualizer.draw_bboxes(
                debug_grids, face_colors=palette, alpha=0.15)

            visualizer.draw_texts(
                list(range(len(debug_grids))),
                debug_grids[:, :2] + 5,
                colors='w')

            visualizer.add_datasample(
                debug_file_name,
                visualizer.get_image(),
                data_sample=merged_result,
                draw_gt=False,
                show=args.show,
                wait_time=0,
                out_file=debug_out_file,
                pred_score_thr=args.score_thr,
            )

            if args.save_patch:
                debug_patch_out_dir = os.path.join(args.out_dir,
                                                   f'{name}_patch')
                for i, slice_result in enumerate(slice_results):
                    patch_out_file = os.path.join(
                        debug_patch_out_dir,
                        f'{filename}_slice_{i}_result.jpg')
                    image = mmcv.imconvert(sliced_image_object.images[i],
                                           'bgr', 'rgb')

                    visualizer.add_datasample(
                        'patch_result',
                        image,
                        data_sample=slice_result,
                        draw_gt=False,
                        show=False,
                        wait_time=0,
                        out_file=patch_out_file,
                        pred_score_thr=args.score_thr,
                    )

        image_result = merge_results_by_nms(
            slice_results,
            sliced_image_object.starting_pixels,
            src_image_shape=(height, width),
            nms_cfg={
                'type': args.merge_nms_type, # 这里是不是能改一下
                'iou_threshold': args.merge_iou_thr
            })
        # 添加面积过滤
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

        # 保存图片可视化

        # visualizer.add_datasample(
        #     filename,
        #     img,
        #     data_sample=image_result,
        #     draw_gt=False,
        #     show=args.show,
        #     wait_time=0,
        #     out_file=out_file,
        #     pred_score_thr=args.score_thr,
        # )

        pred2dict(filename,filtered_result,'/home/star/2T-new/wz/mmdet_dino推理结果存放')

        progress_bar.update()

    if not args.show or (args.debug and args.save_patch):
        print_log(
            f'\nResults have been saved at {os.path.abspath(args.out_dir)}')


if __name__ == '__main__':
    main()
