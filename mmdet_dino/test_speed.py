import time
import cv2
import torch
from mmdet.apis import DetInferencer
from mmdet.evaluation import get_classes
from pprint import pprint

init_args = {
            # 'model': 'configs/mm_grounding_dino/grounding_dino_swin-b_finetune_8xb4_20e_yyc.py',
            # 'weights': 'mmdet_dino_10420_20240722_swinB_30_amp_CosineAnnealingLR_0007/best_coco_bbox_mAP_epoch_25.pth',
            # 'weights': 'mmdet_dino_10420_20240722_swinB_30_amp_CosineAnnealingLR_001_plus_pesudo_81955/best_coco_bbox_mAP_epoch_17.pth',

            'model': '/home/yaoteam/yaoteam/yyc/mmdet_dino/tmp_fasterrcnn/faster-rcnn_x101-32x4d_fpn_1x_coco.py',
            'weights': '/home/yaoteam/yaoteam/yyc/mmdet_dino/tmp_fasterrcnn/best_coco_bbox_mAP_epoch_36.pth',

            # 'weights': 'mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth',
            # 'weights': 'cebaodengft0514_pretrained0512/best_coco_bbox_mAP_epoch_22.pth',
            # 'device': 'cpu',
            'device': 'cuda:0',
            'palette': 'none',
        }

call_args = {
            'inputs': '/home/yaoteam/yaoteam/yyc/yyc_yolov11/test_img.jpg',
            'out_dir': 'outputs',
            'texts': 'insect',
            'pred_score_thr': 0.1,
            'batch_size': 1,
            'no_save_vis': True,
            'no_save_pred': True,
            'print_result': False,
            'custom_entities': False,
            'tokens_positive': None
        }
inferencer = DetInferencer(**init_args)


def run_inference(model, image, device='cuda'):
    inferencer(**call_args)

def measure_fps(model, image, device='cuda', warmup=5, iterations=100):
    # 预热阶段
    for _ in range(warmup):
        run_inference(model, image, device)

    # 正式测量
    start_time = time.time()
    for _ in range(iterations):
        run_inference(model, image, device)
    end_time = time.time()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    fps = 1.0 / avg_time
    return avg_time, fps
# Load a pretrained YOLO11n model
if __name__ == "__main__":


    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    avg_time, fps = measure_fps(None, None, device)

    print(f"Average Inference Time: {avg_time*1000:.2f} ms")
    print(f"FPS: {fps:.2f}\n")