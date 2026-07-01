#!/bin/bash

# 设置 Python 虚拟环境（如果需要）
# source /path/to/your/venv/bin/activate

# 设置变量（可选）
IMAGE_DIR="/home/yaoteam/yaoteam/yyc/mmdet_dino/images_0529_dataugmentation"
CONFIG="configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py"
WEIGHTS="mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth"
TEXT="insect"
OUT_DIR="output0529_dataugmentation"

# 执行推理
python demo/image_demo.py \
    "$IMAGE_DIR" \
    "$CONFIG" \
    --weights "$WEIGHTS" \
    --texts "$TEXT" \
    --pred-score-thr 0.2 \
    --device='cuda:0' \
    --out-dir="$OUT_DIR"