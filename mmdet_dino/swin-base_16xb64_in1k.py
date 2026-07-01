_base_ = [
    'configs/_base_/default_runtime.py'
]
num_classes = 115
# dataset settings
dataset_type = 'CustomDataset'
data_preprocessor = dict(
    num_classes=num_classes,
    # RGB format normalization parameters
    mean=[123.675, 116.28, 103.53],
    std=[58.395, 57.12, 57.375],
    # convert image from BGR to RGB
    to_rgb=True,
)

bgr_mean = data_preprocessor['mean'][::-1]
bgr_std = data_preprocessor['std'][::-1]

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        #A crop of random size (default: of 0.08 to 1.0) of the original size and
        #  a random aspect ratio (default: of 3/4 to 4/3) of the original aspect ratio is made. 
        # This crop is finally resized to given size.
        type='RandomResizedCrop',
        scale=224,
        crop_ratio_range=(0.5,1.0),
        aspect_ratio_range=(3. / 4., 4. / 3.),
        backend='pillow',
        interpolation='bicubic'),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    # dict(
    #     type='GaussianBlur',
    #     magnitude_range=(0.1,2.0,),
    #     magnitude_std='inf',
    #     prob=0.15),
    dict(type='ColorJitter', brightness=0.4, contrast=0.4, saturation=0.5, hue=0.015),
    dict(
        type='RandAugment',
        policies='timm_increasing',
        num_policies=2,
        total_level=10,
        magnitude_level=9,
        magnitude_std=0.5,
        hparams=dict(
            pad_val=[round(x) for x in bgr_mean], interpolation='bicubic')),
    dict(
        type='RandomErasing',
        erase_prob=0.25,
        mode='rand',
        min_area_ratio=0.02,
        max_area_ratio=1 / 3,
        fill_color=bgr_mean,
        fill_std=bgr_std),
    dict(type='PackInputs'),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='ResizeEdge',
        scale=256,
        edge='short',
        backend='pillow',
        interpolation='bicubic'),
    dict(type='CenterCrop', crop_size=224),
    dict(type='PackInputs'),
]

train_dataloader = dict(
    batch_size=128,
    num_workers=8,
    dataset=dict(
        type=dataset_type,
        data_root='/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/训练集/train',
        pipeline=train_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=True),
)

val_dataloader = dict(
    batch_size=128,
    num_workers=8,
    dataset=dict(
        type=dataset_type,
        data_root='/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/训练集/val',
        pipeline=test_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=False),
)
val_evaluator = dict(type='Accuracy', topk=(1, 5))

# If you want standard test, please manually configure the test dataset
test_dataloader = val_dataloader
test_evaluator = val_evaluator



# model settings
model = dict(
    type='ImageClassifier',
    backbone=dict(
        type='SwinTransformer', arch='base', img_size=224, drop_path_rate=0.5),
    neck=dict(type='GlobalAveragePooling'),  
    # neck=dict(        
    #     hid_channels=1024,
    #     in_channels=1024,
    #     num_layers=2,
    #     out_channels=1024,
    #     type='NonLinearNeck',
    #     with_avg_pool=True),    
    head=dict(
        type='LinearClsHead',
        num_classes=num_classes,
        in_channels=1024,
        init_cfg=None,  # suppress the default init_cfg of LinearClsHead.
        loss=dict(
            type='LabelSmoothLoss', label_smooth_val=0.1, mode='original'),
        cal_acc=False),
    init_cfg=[
        dict(type='TruncNormal', layer='Linear', std=0.02, bias=0.),
        dict(type='Constant', layer='LayerNorm', val=1., bias=0.)
    ],
)

# for batch in each gpu is 128, 8 gpu
# lr = 5e-4 * 128 * 8 / 512 = 0.001
optim_wrapper = dict(
    clip_grad=dict(max_norm=5.0),
    optimizer=dict(
        type='AdamW',
        lr=5e-4 * 1024 / 512,
        weight_decay=0.05,
        eps=1e-8,
        betas=(0.9, 0.999)),
    paramwise_cfg=dict(
        norm_decay_mult=0.0,
        bias_decay_mult=0.0,
        flat_decay_mult=0.0,
        custom_keys={
            '.absolute_pos_embed': dict(decay_mult=0.0),
            '.relative_position_bias_table': dict(decay_mult=0.0)
        }),
)

# learning policy
param_scheduler = [
    # warm up learning rate scheduler
    dict(
        type='LinearLR',
        start_factor=1e-3,
        by_epoch=True,
        end=20,
        # update by iter
        convert_to_iter_based=True),
    # main learning rate scheduler
    dict(type='CosineAnnealingLR', eta_min=1e-5, by_epoch=True, begin=20)
]

# train, val, test setting
train_cfg = dict(by_epoch=True, max_epochs=150, val_interval=5)
val_cfg = dict()
test_cfg = dict()

# NOTE: `auto_scale_lr` is for automatically scaling LR,
# based on the actual training batch size.
auto_scale_lr = dict(base_batch_size=1024,enable=True)
# runtime settings
default_hooks = dict(
    # only keeps the latest 3 checkpoints
    checkpoint=dict(type='CheckpointHook', interval=2, max_keep_ckpts=2, save_best='auto'))

# load from which checkpoint
# load_from = '/home/yaoteam/yaoteam/yyc/mmpretrain/work_dirs/simclr_swin/epoch_200.pth'
load_from = '/home/yaoteam/yaoteam/yyc/mmpretrain/swin_base_patch4_window7_224_22kto1k-f967f799.pth'