_base_ = './dino-4scale_r50_8xb2-12e_coco_yyc.py'

pretrained = '/home/star/yyc/mmdetection/checkpoint/swin_large_patch4_window12_384_22k.pth'  # noqa
# pretrained = '/home/star/yyc/mmdetection/checkpoint/swin_tiny_patch4_window7_224.pth'  
num_levels = 5

num_classes = 3
data_root = '/home/star/gyf/mmdetection_latest/mmdetection/data/gzimg-win/'
class_name = ('xce', 'tj', 'yl')
metainfo = dict(classes=class_name, palette=[(220, 20, 60)]) # 这个是干嘛用的？
# 36 epoch 注释掉的话即为默认的12epoch
max_epochs = 36
default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=2, save_best='auto'),
    logger=dict(type='LoggerHook', interval=200))
train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=max_epochs, val_interval=1)
param_scheduler = [
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_epochs,
        by_epoch=True,
        milestones=[27, 33],
        gamma=0.1)
]



# swint
model = dict(
    num_feature_levels=num_levels,
    backbone=dict(
        _delete_=True,
        type='SwinTransformer',
        pretrain_img_size=384,
        embed_dims=192,
        depths=[2, 2, 18, 2],
        num_heads=[6, 12, 24, 48],
        window_size=12,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        # Please only add indices that would be used
        # in FPN, otherwise some parameter will not be used
        with_cp=True,
        convert_weights=True,
        init_cfg=dict(type='Pretrained', checkpoint=pretrained)),
    neck=dict(in_channels=[192, 384, 768, 1536], num_outs=num_levels),
    encoder=dict(layer_cfg=dict(self_attn_cfg=dict(num_levels=num_levels))),
    decoder=dict(layer_cfg=dict(cross_attn_cfg=dict(num_levels=num_levels))),
    bbox_head=dict(num_classes=num_classes))
# # swinL
# model = dict(
#     num_feature_levels=num_levels,
#     backbone=dict(
#         _delete_=True,
#         type='SwinTransformer',
#         pretrain_img_size=384,
#         embed_dims=192,
#         depths=[2, 2, 18, 2],
#         num_heads=[6, 12, 24, 48],
#         window_size=12,
#         mlp_ratio=4,
#         qkv_bias=True,
#         qk_scale=None,
#         drop_rate=0.,
#         attn_drop_rate=0.,
#         drop_path_rate=0.2,
#         patch_norm=True,
#         out_indices=(0, 1, 2, 3),
#         # Please only add indices that would be used
#         # in FPN, otherwise some parameter will not be used
#         with_cp=True,
#         convert_weights=True,
#         init_cfg=dict(type='Pretrained', checkpoint=pretrained)),
#     neck=dict(in_channels=[192, 384, 768, 1536], num_outs=num_levels),
#     encoder=dict(layer_cfg=dict(self_attn_cfg=dict(num_levels=num_levels))),
#     decoder=dict(layer_cfg=dict(cross_attn_cfg=dict(num_levels=num_levels))))



train_dataloader = dict(
    batch_size=1,  # 单个 GPU 的 batch size
    num_workers=8,  # 单个 GPU 分配的数据加载线程数
    dataset=dict(
        type='CocoDataset',
        data_root=data_root,
        metainfo=metainfo,
        return_classes=True,
        ann_file=data_root + 'annotations/train_.json',
        data_prefix=dict(img='train/')
        ))
val_dataloader = dict(
    batch_size=1,  # 单个 GPU 的 batch size
    num_workers=8,  # 单个 GPU 分配的数据加载线程数
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file=data_root + 'annotations/val.json',
        data_prefix=dict(img='train/')))
test_dataloader = val_dataloader

val_evaluator = dict(ann_file=data_root + 'annotations/val.json')
test_evaluator = val_evaluator
# 预训练模型
load_from = '/home/star/yyc/mmdetection/dino-5scale_swin-l_8xb2-36e_coco-5486e051.pth'


# 从哪个check points跑，会覆盖load_from
# resume_from = 'weight/img5/cascade/latest.pth'
# work_dir = 'weight/my-cascade/new-img1'