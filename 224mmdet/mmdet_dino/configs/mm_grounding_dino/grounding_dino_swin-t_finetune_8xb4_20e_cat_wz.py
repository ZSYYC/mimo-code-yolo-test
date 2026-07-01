_base_ = 'grounding_dino_swin-b_pretrain_obj365_goldg_v3det.py'
# _base_ = 'grounding_dino_swin-t_pretrain_obj365.py'

data_root = '/home/star/2T-new/wz/groundingdino微调/'
# 具体的命名要按照标注文件json中的categories一栏来一个一个填
# class_name = ('Chilo-suppressalis', 'Macroceroea-grandis-Gray', 'Rice-leaf-folder', 'Sesamia-inferens', 'Sirthenea-flavipes', 'brown-planthopper', 'lacewing-fly', 'small-brown-planthopper', 'white-backed-planthopper', )
# class_name = ('dzjym','hmbb','1','ehm')
class_name = ('insect',)
# palette = [(255, 97, 0), (0, 201, 87), (176, 23, 31), (138, 43, 226),
#            (30, 144, 255)]  # 对应类的调色板
num_classes = len(class_name)
metainfo = dict(classes=class_name, palette=[(220, 20, 60), (255, 20, 60), (220, 255, 60), (220, 20, 255), ])

model = dict(bbox_head=dict(num_classes=num_classes))

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    # dict(type='ColorJitter', brightness=0.4, contrast=0.4, saturation=0.4, hue=0.015),
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
                    scales=[(400, 4200), (500, 4200), (600, 4200)],
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
# train_pipeline = [
#     dict(type='LoadImageFromFile'),
#     dict(type='LoadAnnotations', with_bbox=True),
#
#     dict(type='RandomFlip', prob=0.5),
#
#     dict(
#         type='PhotoMetricDistortion',
#         brightness_delta=20,
#         contrast_range=(0.9, 1.1),
#         saturation_range=(0.9, 1.1),
#         hue_delta=5),
#
#     dict(
#         type='Resize',
#         scale=(800, 1333),
#         keep_ratio=True),
#
#     dict(
#         type='PackDetInputs',
#         meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
#                        'scale_factor', 'flip', 'flip_direction', 'text',
#                        'custom_entities'))
# ]
test_pipeline = [
    dict(
        type='LoadImageFromFile', backend_args=None,
        imdecode_backend='pillow'),
    dict(
        type='mmdet.FixScaleResize',
        scale=(800, 1333),
        keep_ratio=True,
        backend='pillow'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='mmdet.PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'text', 'custom_entities',
                   'tokens_positive'))
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

# total images -> 10752
dataset_10000 = dict(
    type='CocoDataset',
    data_root=data_root,
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    filter_cfg=dict(filter_empty_gt=False, min_size=32),
    ann_file=data_root + 'annotations/instances_train.json',
    data_prefix=dict(img=data_root + 'train/'))
# dataset_10000=dict(
#     type='CocoDataset',
#     data_root=data_root,
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     filter_cfg=dict(filter_empty_gt=False, min_size=32),
#     ann_file='annotations/coco_train.json',
#     data_prefix=dict(img='train/'))

train_dataloader = dict(
    _delete_=True,
    batch_size=4,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(type='ConcatDataset', datasets=[dataset_10000, ]))

val_dataloader = dict(
    _delete_=True,
    batch_size=4,
    num_workers=4,
    dataset=dict(
        metainfo=metainfo,
        type='CocoDataset',
        test_mode=True,
        pipeline=test_pipeline,
        return_classes=True,
        data_root=data_root,
        ann_file=data_root + 'annotations/instances_val.json',
        data_prefix=dict(img=data_root + 'val/')))

test_dataloader = val_dataloader

val_evaluator = dict(ann_file=data_root + 'annotations/instances_val.json')
test_evaluator = val_evaluator

max_epoch = 40

default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=1, save_best='auto'),
    logger=dict(type='LoggerHook', interval=100))
train_cfg = dict(max_epochs=max_epoch,  # 最大训练轮次
                 val_interval=1)  # 验证间隔。每个 epoch 验证一次

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
# load_from = '/home/star/yyc/mmdet_dino/mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth'
