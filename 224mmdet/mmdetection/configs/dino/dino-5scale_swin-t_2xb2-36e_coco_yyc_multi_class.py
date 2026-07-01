_base_ = './dino-4scale_r50_8xb2-12e_coco_yyc_multi_class.py'

# pretrained = '/home/star/yyc/mmdetection/checkpoint/InsectSSRL_Swin_T_student.pth'  
pretrained = '/home/star/yyc/mmdetection/checkpoint/swin_tiny_patch4_window7_224.pth'  
num_levels = 5


# 36 epoch 注释掉的话即为默认的12epoch
max_epochs = 36
default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=2, save_best='auto'),
    logger=dict(type='LoggerHook', interval=10))
train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=max_epochs, val_interval=18)
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
        pretrain_img_size=224,
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        frozen_stages=-1,# 1：第一个 stage 权重固定 -1：不固定
        out_indices=(1, 2, 3),
        # Please only add indices that would be used
        # in FPN, otherwise some parameter will not be used
        with_cp=True,
        convert_weights=True,
        init_cfg=dict(type='Pretrained', checkpoint=pretrained)),
    neck=dict(in_channels=[192, 384, 768], num_outs=num_levels),
    encoder=dict(layer_cfg=dict(self_attn_cfg=dict(num_levels=num_levels))),
    decoder=dict(layer_cfg=dict(cross_attn_cfg=dict(num_levels=num_levels))))
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


