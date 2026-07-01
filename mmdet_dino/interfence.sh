#! /bin/bash

# python demo/image_demo.py /home/yaoteam/yaoteam/yyc/mmdet_dino/images/test_img0606 \
#         cebaodengft0512/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
#         --weights cebaodengft0514_pretrained0512/best_coco_bbox_mAP_epoch_22.pth\
#         --texts 'insect' \
#         --pred-score-thr 0.4


python demo/large_image_demo.py \
	/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/images \
	configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
	mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth \
	--device cuda:0  \
	--score-thr 0.3 \
	--patch-size 800 \
	--patch-overlap-ratio 0.1 \
	--merge-iou-thr 0.25 \
	--merge-nms-type nms \
	--batch-size 8 --out-dir ./sahi模型幻觉论文用途研究swint/images

python demo/large_image_demo.py \
	/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/output \
	configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
	mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth \
	--device cuda:0  \
	--score-thr 0.3 \
	--patch-size 800 \
	--patch-overlap-ratio 0.1 \
	--merge-iou-thr 0.25 \
	--merge-nms-type nms \
	--batch-size 8 --out-dir ./sahi模型幻觉论文用途研究swint/output

python demo/large_image_demo.py \
	/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/output255 \
	configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
	mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth \
	--device cuda:0  \
	--score-thr 0.3 \
	--patch-size 800 \
	--patch-overlap-ratio 0.1 \
	--merge-iou-thr 0.25 \
	--merge-nms-type nms \
	--batch-size 8 --out-dir ./sahi模型幻觉论文用途研究swint/output255

python demo/large_image_demo.py \
	/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/output_white \
	configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py \
	mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth \
	--device cuda:0  \
	--score-thr 0.3 \
	--patch-size 800 \
	--patch-overlap-ratio 0.1 \
	--merge-iou-thr 0.25 \
	--merge-nms-type nms \
	--batch-size 8 --out-dir ./sahi模型幻觉论文用途研究swint/output_white