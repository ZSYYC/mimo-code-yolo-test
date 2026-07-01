_base_ = 'grounding_dino_swin-b_pretrain_obj365_goldg_v3det.py'

data_root = '/home/star/8T/yyc/dataset/分离出来的数据集0616_10000/'
# 具体的命名要按照标注文件json中的categories一栏来一个一个填
# class_name = ('Chilo-suppressalis', 'Macroceroea-grandis-Gray', 'Rice-leaf-folder', 'Sesamia-inferens', 'Sirthenea-flavipes', 'brown-planthopper', 'lacewing-fly', 'small-brown-planthopper', 'white-backed-planthopper', )
class_name = ('insect',)
# palette = [(255, 97, 0), (0, 201, 87), (176, 23, 31), (138, 43, 226),
#            (30, 144, 255)]  # 对应类的调色板
num_classes = len(class_name)
metainfo = dict(classes=class_name, palette=[(220, 20, 60)])

model = dict(bbox_head=dict(num_classes=num_classes))

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    # dict(type='ColorJitter', brightness=0.4, contrast=0.4, saturation=0.2, hue=0.015),
    dict(type='RandomChoice',
         transforms=[
            [
                dict(type='PhotoMetricDistortion', 
                      brightness_delta=32,
                      contrast_range=(0.5, 1.5),
                      saturation_range=(0.5, 1.5),
                      hue_delta=18),
            ],
            [
                dict(
                    # 使用之前要pip install imagecorruptions 和 albumentations
                    type='Corrupt',
                    corruption='gaussian_noise',
                    severity=1
                )
            ],
            [
                dict(
                    # 使用之前要pip install imagecorruptions 和 albumentations
                    type='Corrupt',
                    corruption='defocus_blur',
                    severity=1
                )
            ],
            [
                dict(
                    # 使用之前要pip install imagecorruptions 和 albumentations
                    type='Corrupt',
                    corruption='impulse_noise',
                    severity=1
                )
            ],
         ]
         ),
    
    dict(
        type='RandomChoice',
        transforms=[
            [
                dict(
                    type='RandomChoiceResize',
                    scales=[(480, 1333), (512, 1333), (544, 1333), (576, 1333),
                            (608, 1333), (640, 1333), (672, 1333), (704, 1333),
                            (736, 1333), (768, 1333), (800, 1333)],
                    keep_ratio=True)
            ],
            [
                dict(
                    type='RandomChoiceResize',
                    # The radio of all image in train dataset < 7
                    # follow the original implement
                    scales=[(400, 4200), (500, 4200), (600, 4200),(700, 4200), (800, 4200), (900, 4200),
                            (1000, 4200), (1200, 4200), (1400, 4200),(1600, 4200), (1800, 4200), (2000, 4200),
                            (3000, 4200)],
                    # scales=[(400, 4200), (500, 4200), (600, 4200)],
                    keep_ratio=True),
                dict(
                    type='RandomCrop',
                    crop_type='absolute_range',
                    crop_size=(384, 600),
                    allow_negative_crop=True),
                dict(
                    type='RandomChoiceResize',
                    scales=[(480, 1333), (512, 1333), (544, 1333), (576, 1333),
                            (608, 1333), (640, 1333), (672, 1333), (704, 1333),
                            (736, 1333), (768, 1333), (800, 1333)],
                    keep_ratio=True)
            ]
        ]),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'flip', 'flip_direction', 'text',
                   'custom_entities'))
]

# train_dataloader = dict(
#     dataset=dict(
#         _delete_=True,
#         type='CocoDataset',
#         data_root=data_root,
#         metainfo=metainfo,
#         return_classes=True,
#         pipeline=train_pipeline,
#         filter_cfg=dict(filter_empty_gt=False, min_size=32),
#         ann_file='annotations/train2017.json',
#         data_prefix=dict(img='images/')))

dataset_10000=dict(
    type='CocoDataset',
    data_root=data_root,
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    filter_cfg=dict(filter_empty_gt=False, min_size=32),
    ann_file='annotations/train2017.json',
    data_prefix=dict(img='images/'))
dataset_420=dict(
    type='CocoDataset',
    data_root='/home/star/2T/yyc/cebaodengft0514_420',
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    filter_cfg=dict(filter_empty_gt=False, min_size=32),
    ann_file='annotations/train2017.json',
    data_prefix=dict(img='images/'))
dataset_pesudo_81955=dict(
    type='CocoDataset',
    data_root='/home/star/2T/outputs_pesudo_81955',
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    filter_cfg=dict(filter_empty_gt=False, min_size=32),
    ann_file='annotations/train2017.json',
    data_prefix=dict(img='images/'))
dataset_132_fzl50_danzhongchong=dict(
    type='CocoDataset',
    data_root='/home/star/2T/yyc/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs',
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    filter_cfg=dict(filter_empty_gt=False, min_size=32),
    ann_file='annotations/train2017.json',
    data_prefix=dict(img='images/'))
background_xiaochong200=dict(
    type='CocoDataset',
    data_root='/home/star/2T/yyc/背景图和分离出的小虫图/小虫背景训练集mmdet_dino',
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    filter_cfg=dict(filter_empty_gt=False, min_size=32), # 是否过滤掉不包含 GT 的图片
    ann_file='annotations/train2017.json',
    data_prefix=dict(img='images/'))

train_dataloader = dict(
    batch_size=4,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(type='ConcatDataset', datasets=[dataset_10000,dataset_420,dataset_pesudo_81955,dataset_132_fzl50_danzhongchong,background_xiaochong200]))



test_pipeline = [
    dict(
        type='LoadImageFromFile', backend_args=None,
        imdecode_backend='pillow'),
    dict(
        type='FixScaleResize',
        scale=(800, 1333),
        keep_ratio=True,
        backend='pillow'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'text', 'custom_entities',
                   'tokens_positive'))
]
val_dataloader = dict(
    batch_size=4,
    num_workers=8,
    dataset=dict(
        metainfo=metainfo,
        type='CocoDataset',
        test_mode=True,
        pipeline=test_pipeline,
        return_classes=True,
        data_root=data_root,
        ann_file='annotations/val2017.json',
        data_prefix=dict(img='images/')))

test_dataloader = val_dataloader

val_evaluator = dict(ann_file=data_root + 'annotations/val2017.json')
test_evaluator = val_evaluator

max_epoch = 20

default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=1, save_best='auto'),
    logger=dict(type='LoggerHook', interval=100))
train_cfg = dict(max_epochs=max_epoch, # 最大训练轮次
                 val_interval=1) # 验证间隔。每个 epoch 验证一次

param_scheduler = [
    # dict(type='LinearLR', start_factor=0.1, by_epoch=False, begin=0, end=1000),
    # dict(
    #     type='MultiStepLR',
    #     begin=0,
    #     end=max_epoch,
    #     by_epoch=True,
    #     milestones=[13, 16],
    #     gamma=0.1)
    dict(T_max=20, begin=0, by_epoch=True, end=20, type='CosineAnnealingLR')
]

optim_wrapper = dict(
    optimizer=dict(lr=0.0007, type='AdamW', weight_decay=0.0001),
    # optimizer=dict(lr=0.001, type='AdamW', weight_decay=0.0001),
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'backbone': dict(lr_mult=0.0),
            'language_model': dict(lr_mult=0.0)
        }))

load_from = '/home/star/yyc/mmdet_dino/grounding_dino_swin-b_pretrain_obj365_goldg_v3de-f83eef00.pth'  # noqa

# torchrun --nproc_per_node 4 --master_port=25641 tools/train.py configs/mm_grounding_dino/grounding_dino_swin-b_finetune_8xb4_20e_yyc.py --work-dir mmdet_dino_10420_20240722_swinB_30_amp_CosineAnnealingLR_001_plus_pesudo_81955 --auto-scale-lr --launcher 'pytorch' --amp