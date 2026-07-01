_base_ = [
    '../_base_/default_runtime.py',
]

# dataset settings
# dataset settings
dataset_type = 'CustomDataset'
data_root = '/home/yaoteam/yaoteam/yyc/random_paste_work/all_small_images_unlabeled_240524'
data_preprocessor = dict(
    type='SelfSupDataPreprocessor',
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    to_rgb=True)

# the difference between ResNet50 and ViT pipeline is the `scale` in
# `RandomResizedCrop`, `scale=(0.08, 1.)` in ViT pipeline
view_pipeline1 = [
    dict(
        type='RandomResizedCrop',
        scale=224,
        # crop_ratio_range=(0.08, 1.), 这里要做出修改，view_pipeline2下同
        crop_ratio_range=(0.5, 1.),
        backend='pillow'),
    dict(
        type='RandomApply',
        transforms=[
            dict(
                type='ColorJitter',
                brightness=0.4,
                contrast=0.4,
                saturation=0.2, # 后续看看能不能改
                hue=0.1)
        ],
        prob=0.8),
    dict(
        type='RandomGrayscale',
        prob=0.2,
        keep_channels=True,
        channel_weights=(0.114, 0.587, 0.2989)),
    dict(
        type='GaussianBlur',
        magnitude_range=(0.1, 2.0),
        magnitude_std='inf',
        prob=1.),
    dict(type='Solarize', thr=128, prob=0.),
    dict(type='RandomFlip', prob=0.5),
]
view_pipeline2 = [
    dict(
        type='RandomResizedCrop',
        scale=224,
        # crop_ratio_range=(0.08, 1.),
        crop_ratio_range=(0.5, 1.),
        backend='pillow'),
    dict(
        type='RandomApply',
        transforms=[
            dict(
                type='ColorJitter',
                brightness=0.4,
                contrast=0.4,
                saturation=0.2,
                hue=0.1)
        ],
        prob=0.8),
    dict(
        type='RandomGrayscale',
        prob=0.2,
        keep_channels=True,
        channel_weights=(0.114, 0.587, 0.2989)),
    dict(
        type='GaussianBlur',
        magnitude_range=(0.1, 2.0),
        magnitude_std='inf',
        prob=0.1),
    dict(type='Solarize', thr=128, prob=0.2),
    dict(type='RandomFlip', prob=0.5),
]

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiView',
        num_views=[1, 1],
        transforms=[view_pipeline1, view_pipeline2]),
    dict(type='PackInputs')
]
train_dataloader = dict(
    batch_size=256,
    num_workers=8,
    persistent_workers=True,
    pin_memory=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    collate_fn=dict(type='default_collate'),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='',       # We assume you are using the sub-folder format without ann_file,我们假设您使用的是没有ann_file的子文件夹格式
        data_prefix='',    # The `data_root` is the data_prefix directly. 参考https://blog.csdn.net/qq_41627642/article/details/131561433
        with_label=False,
        pipeline=train_pipeline))

# model settings
temperature = 0.2
model = dict(
    type='MoCoV3',
    base_momentum=0.01,
    backbone=dict(
        type='MoCoV3ViT',
        arch='mocov3-small',  # embed_dim = 384
        img_size=224,
        patch_size=16,
        stop_grad_conv1=True),
    neck=dict(
        type='NonLinearNeck',
        in_channels=384,
        hid_channels=4096,
        out_channels=256,
        num_layers=3,
        with_bias=False,
        with_last_bn=True,
        with_last_bn_affine=False,
        with_last_bias=False,
        with_avg_pool=False),
    head=dict(
        type='MoCoV3Head',
        predictor=dict(
            type='NonLinearNeck',
            in_channels=256,
            hid_channels=4096,
            out_channels=256,
            num_layers=2,
            with_bias=False,
            with_last_bn=True,
            with_last_bn_affine=False,
            with_last_bias=False,
            with_avg_pool=False),
        loss=dict(type='CrossEntropyLoss', loss_weight=2 * temperature),
        temperature=temperature))

# optimizer
optim_wrapper = dict(
    type='AmpOptimWrapper',
    loss_scale='dynamic',
    optimizer=dict(type='AdamW', lr=2.4e-3, weight_decay=0.1))
find_unused_parameters = True

# learning rate scheduler
param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=1e-4,
        by_epoch=True,
        begin=0,
        end=40,
        convert_to_iter_based=True),
    dict(
        type='CosineAnnealingLR',
        T_max=260,
        by_epoch=True,
        begin=40,
        end=300,
        convert_to_iter_based=True)
]

# runtime settings
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=300)
# only keeps the latest 3 checkpoints
default_hooks = dict(checkpoint=dict(max_keep_ckpts=3))
load_from='/home/yaoteam/yaoteam/yyc/mmpretrain0624/mocov3_vit-small-p16_16xb256-amp-coslr-300e_in1k-224_20220826-08bc52f7.pth'
# NOTE: `auto_scale_lr` is for automatically scaling LR
# based on the actual training batch size.
auto_scale_lr = dict(base_batch_size=4096,enable=True)
