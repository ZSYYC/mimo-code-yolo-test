#! /bin/bash
torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py --work-dir /home/star/2T/lilingyi/GDINO_output --auto-scale-lr --launcher 'pytorch' --amp 

python demo/image_demo.py /home/star/2T/lilingyi/GroundingDINO/rice_dataset/val \
        configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
        --weights /home/star/2T/lilingyi/GDINO_output/best_coco_bbox_mAP_epoch_25.pth\
        --texts 'ehm. dzjym. hmbb. 1. ' \
        --pred-score-thr 0.25 \
--device='cuda:1' \
--out-dir='/home/star/2T/lilingyi/GDINO_output'