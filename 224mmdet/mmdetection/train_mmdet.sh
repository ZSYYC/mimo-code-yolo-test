#! /bin/bash
# conda activate wz_mmdet
# python jiankongyyc.py
# sleep 1
# torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/dino/dino-5scale_swin-t_2xb2-36e_coco_yyc_multi_class.py --work-dir  /home/star/2T/yyc/exp3_20251020/train_result/dino_swint_multi_class_36ep --auto-scale-lr --launcher 'pytorch' --resume
# sleep 5
# torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/dino/dino-5scale_swin-t_2xb2-36e_coco_yyc.py --work-dir  /home/star/2T/yyc/exp3_20251020/train_result/dino_swint_singleclass_36ep --auto-scale-lr --launcher 'pytorch'
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun --nproc_per_node 4 --master_port=25633 tools/train.py configs/faster_rcnn/faster-rcnn_x101-32x4d_fpn_1x_coco.py --work-dir  /home/star/2T/yyc/exp3_20251020/faster_rcnn_36_r101_500_coco_multiclass --auto-scale-lr --launcher 'pytorch' --amp
# 没问题，已经测试过了
# python demo/image_demo.py /home/star/2T-new/yyc/exp3_20251020/coco_dataset_split/val2017/3_23-07-09-17-35-21_0_82b10-3.jpg \
# /home/star/2T-new/yyc/exp3_20251020/dino_swint_singleclass_36ep/dino-5scale_swin-t_2xb2-36e_coco_yyc.py \
# --weights /home/star/2T-new/yyc/exp3_20251020/dino_swint_singleclass_36ep/best_coco_bbox_mAP_epoch_33.pth \
# --device cuda:0
# 存在问题，需要修改
# python demo/image_demo.py /home/star/2T-new/yyc/exp3_20251020/coco_dataset_split/val2017/3_23-07-09-17-35-21_0_82b10-3.jpg \
# /home/star/2T-new/yyc/exp3_20251020/dino_swint_multi_class_36ep/dino-5scale_swin-t_2xb2-36e_coco_yyc_multi_class.py \
# --weights /home/star/2T-new/yyc/exp3_20251020/dino_swint_multi_class_36ep_old/epoch_21.pth \
# --device cuda:0


# python tools/test.py /home/star/2T-new/yyc/exp3_20251020/dino_swint_multi_class_36ep/dino-5scale_swin-t_2xb2-36e_coco_yyc_multi_class.py \
# /home/star/2T-new/yyc/exp3_20251020/dino_swint_multi_class_36ep_old/epoch_21.pth