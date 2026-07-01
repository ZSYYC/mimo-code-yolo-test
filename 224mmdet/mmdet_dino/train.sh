#! /bin/bash
# torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/mm_grounding_dino/grounding_dino_swin-b_finetune_8xb4_20e_yyc.py --work-dir /home/star/8T/yyc/mmdet_dino_model_cache --auto-scale-lr --launcher 'pytorch'
python jiankongyyc.py
sleep 5
#torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/dino/dino-5scale_swin-l_2xb2-36e_coco_yyc.py --work-dir /home/star/8T/yyc/dinoL_12ep_5dataset_model_cache --auto-scale-lr --launcher 'pytorch' --amp
torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat_wz.py --work-dir /home/star/2T-new/wz/groundingdino微调/ --launcher 'pytorch' --amp
