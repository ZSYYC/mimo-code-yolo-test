from mmdet.apis import DetInferencer

# models 是一个模型名称列表，它们将自动打印
# models = DetInferencer.list_models('mmdet')
# print(models)
inferencer = DetInferencer(model='/home/yaoteam/yaoteam/yyc/mmdetection/configs/dino/dino-5scale_swin-l_8xb2-12e_coco.py', 
                           weights='/home/yaoteam/yaoteam/yyc/mmdetection/checkpoint/dino-5scale_swin-l_8xb2-12e_coco_20230228_072924-a654145f.pth',
                           device='cuda:0')
inferencer('demo/insect.jpg', out_dir='outputs/', no_save_pred=True)


# 初始化模型
# inferencer = DetInferencer('rtmdet_tiny_8xb32-300e_coco')

# 推理示例图片
# inferencer('demo/demo.jpg', show=True)

