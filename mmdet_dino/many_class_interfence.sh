#!/bin/bash

# 设置输入文件夹和输出文件夹的路径
INPUT_DIR="/home/yaoteam/yaoteam/yyc/mmdet_dino/mosquito"
OUTPUT_DIR="/home/yaoteam/yaoteam/yyc/mmdet_dino/mosquito_output"

# 设置其他固定参数
SCRIPT_PATH="configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py"
# WEIGHTS_PATH="cebaodengft0514_pretrained0512/best_coco_bbox_mAP_epoch_22.pth"
WEIGHTS_PATH="grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth"
TEXTS="insect"
PRED_SCORE_THR=0.25
DEVICE="cuda:0"
# 设置环境变量
export CUDA_VISIBLE_DEVICES=1

# 遍历输入文件夹下的所有子文件夹
for SUBDIR in "$INPUT_DIR"/*; do
    if [ -d "$SUBDIR" ]; then
        # 获取子文件夹名
        SUBDIR_NAME=$(basename "$SUBDIR")
        
        # 构造输出文件夹路径
        OUT_DIR="$OUTPUT_DIR/$SUBDIR_NAME"
        
        # 创建输出文件夹
        mkdir -p "$OUT_DIR"
        
        # 打印处理信息
        echo "Processing $SUBDIR_NAME..."
        
        # 执行Python脚本
        python demo/image_demo.py "$SUBDIR" \
            "$SCRIPT_PATH" \
            --weights "$WEIGHTS_PATH" \
            --texts "$TEXTS" \
            --pred-score-thr "$PRED_SCORE_THR" \
            --out-dir "$OUT_DIR" \
            --device "$DEVICE"
        
        # 等待Python脚本执行完毕
        wait
        
        # 打印完成信息
        echo "$SUBDIR_NAME processed."
    fi
done

echo "All subfolders processed."
