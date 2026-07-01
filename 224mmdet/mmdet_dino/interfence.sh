#! /bin/bash

python demo/image_demo.py /home/yaoteam/yaoteam/yyc/mmdet_dino/images/test_img0606 \
        cebaodengft0512/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
        --weights cebaodengft0514_pretrained0512/best_coco_bbox_mAP_epoch_22.pth\
        --texts 'insect' \
        --pred-score-thr 0.4
