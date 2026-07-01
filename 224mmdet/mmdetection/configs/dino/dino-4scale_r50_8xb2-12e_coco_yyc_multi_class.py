_base_ = [
    '../_base_/datasets/coco_detection.py', '../_base_/default_runtime.py'
]
# 具体的命名要按照标注文件json中的categories一栏来一个一个填 
num_classes =  751
class_name = ('B10', 'B12', 'B121', 'B13', 'B133', 'B135', 'B138', 'B139', 'B14', 'B140', 'B15', 'B150', 'B152', 'B153', 'B154', 'B155', 'B156', 'B157', 'B158', 'B159', 'B160', 'B161', 'B162', 'B163', 'B164', 'B165', 'B166', 'B167', 'B168', 'B169', 'B17', 'B170', 'B171', 'B172', 'B173', 'B174', 'B175', 'B176', 'B177', 'B178', 'B179', 'B18', 'B180', 'B181', 'B182', 'B183', 'B184', 'B185', 'B186', 'B187', 'B188', 'B189', 'B19', 'B190', 'B191', 'B2', 'B200', 'B22', 'B23', 'B24', 'B26', 'B27', 'B28', 'B3', 'B30', 'B32', 'B39', 'B4', 'B40', 'B42', 'B49', 'B5', 'B6', 'B60', 'B8', 'B88', 'B9', 'B96', 'B97', 'B98', 'FL1', 'FL17', 'FL18', 'FL19', 'FL20', 'FL3', 'FL7', 'FY1', 'FY5', 'G2', 'GE1', 'GE2', 'GE3', 'L1', 'L10', 'L100', 'L1000', 'L1001', 'L1002', 'L1003', 'L1004', 'L103', 'L104', 'L105', 'L106', 'L107', 'L108', 'L109', 'L11', 'L114', 'L115', 'L117', 'L119', 'L12', 'L120', 'L123', 'L126', 'L127', 'L129', 'L130', 'L132', 'L134', 'L136', 'L137', 'L138', 'L14', 'L140', 'L142', 'L147', 'L148', 'L149', 'L15', 'L150', 'L151', 'L152', 'L157', 'L158', 'L159', 'L16', 'L160', 'L161', 'L164', 'L165', 'L166', 'L167', 'L169', 'L17', 'L171', 'L178', 'L18', 'L180', 'L181', 'L182', 'L185', 'L188', 'L189', 'L19', 'L190', 'L192', 'L193', 'L194', 'L197', 'L199', 'L2', 'L20', 'L201', 'L202', 'L204', 'L205', 'L206', 'L207', 'L208', 'L209', 'L21', 'L210', 'L211', 'L214', 'L216', 'L218', 'L22', 'L227', 'L229', 'L23', 'L24', 'L26', 'L27', 'L28', 'L29', 'L30', 'L31', 'L32', 'L33', 'L333', 'L334', 'L34', 'L342', 'L343', 'L344', 'L347', 'L35', 'L350', 'L351', 'L352', 'L353', 'L355', 'L357', 'L36', 'L360', 'L361', 'L365', 'L368', 'L369', 'L37', 'L374', 'L38', 'L383', 'L39', 'L393', 'L396', 'L398', 'L4', 'L40', 'L404', 'L41', 'L419', 'L421', 'L429', 'L43', 'L435', 'L44', 'L440', 'L452', 'L454', 'L458', 'L46', 'L463', 'L47', 'L472', 'L483', 'L484', 'L49', 'L491', 'L5', 'L50', 'L506', 'L51', 'L512', 'L52', 'L522', 'L53', 'L539', 'L54', 'L548', 'L55', 'L554', 'L559', 'L561', 'L566', 'L567', 'L57', 'L571', 'L573', 'L58', 'L583', 'L587', 'L590', 'L593', 'L597', 'L6', 'L60', 'L63', 'L64', 'L643', 'L650', 'L654', 'L659', 'L666', 'L67', 'L670', 'L671', 'L672', 'L683', 'L686', 'L689', 'L692', 'L696', 'L7', 'L707', 'L708', 'L72', 'L720', 'L741', 'L746', 'L747', 'L75', 'L76', 'L760', 'L761', 'L762', 'L763', 'L764', 'L765', 'L766', 'L767', 'L768', 'L769', 'L77', 'L770', 'L771', 'L772', 'L773', 'L774', 'L775', 'L776', 'L777', 'L778', 'L779', 'L780', 'L781', 'L782', 'L783', 'L784', 'L785', 'L786', 'L787', 'L788', 'L789', 'L79', 'L790', 'L791', 'L792', 'L793', 'L794', 'L795', 'L796', 'L797', 'L798', 'L799', 'L8', 'L800', 'L801', 'L802', 'L803', 'L804', 'L805', 'L806', 'L807', 'L808', 'L809', 'L81', 'L810', 'L811', 'L812', 'L813', 'L815', 'L816', 'L817', 'L818', 'L819', 'L82', 'L820', 'L821', 'L822', 'L823', 'L824', 'L825', 'L826', 'L827', 'L828', 'L829', 'L830', 'L831', 'L832', 'L833', 'L834', 'L835', 'L836', 'L837', 'L838', 'L839', 'L84', 'L840', 'L841', 'L842', 'L843', 'L844', 'L845', 'L846', 'L847', 'L848', 'L849', 'L85', 'L850', 'L851', 'L852', 'L853', 'L854', 'L855', 'L856', 'L857', 'L858', 'L859', 'L86', 'L860', 'L861', 'L862', 'L863', 'L864', 'L865', 'L866', 'L867', 'L868', 'L869', 'L87', 'L870', 'L871', 'L872', 'L873', 'L874', 'L875', 'L876', 'L877', 'L878', 'L879', 'L880', 'L881', 'L882', 'L883', 'L884', 'L885', 'L886', 'L887', 'L888', 'L889', 'L890', 'L892', 'L893', 'L894', 'L895', 'L896', 'L897', 'L898', 'L899', 'L9', 'L90', 'L900', 'L901', 'L902', 'L903', 'L904', 'L905', 'L906', 'L907', 'L908', 'L909', 'L91', 'L910', 'L911', 'L912', 'L913', 'L914', 'L915', 'L916', 'L917', 'L918', 'L919', 'L92', 'L920', 'L921', 'L922', 'L923', 'L924', 'L925', 'L926', 'L927', 'L928', 'L929', 'L93', 'L930', 'L931', 'L932', 'L933', 'L934', 'L935', 'L936', 'L937', 'L938', 'L939', 'L94', 'L940', 'L941', 'L942', 'L943', 'L944', 'L945', 'L946', 'L947', 'L948', 'L949', 'L95', 'L950', 'L951', 'L952', 'L953', 'L954', 'L955', 'L956', 'L957', 'L958', 'L959', 'L96', 'L960', 'L961', 'L962', 'L963', 'L964', 'L965', 'L966', 'L967', 'L968', 'L969', 'L97', 'L970', 'L971', 'L972', 'L973', 'L974', 'L975', 'L976', 'L977', 'L978', 'L979', 'L980', 'L981', 'L982', 'L983', 'L984', 'L985', 'L986', 'L987', 'L988', 'L989', 'L990', 'L999', 'M6', 'MAO1', 'MAO2', 'MAO5', 'MAO6', 'MAO7', 'MAO8', 'MO3', 'MO31', 'MO38', 'MO39', 'MO40', 'MO41', 'MO43', 'MO45', 'MO46', 'MO47', 'MO48', 'MO6', 'MO7', 'MO8', 'MO9', 'MV1', 'MV10', 'MV11', 'MV12', 'MV13', 'MV14', 'MV15', 'MV17', 'MV18', 'MV19', 'MV2', 'MV20', 'MV21', 'MV22', 'MV23', 'MV24', 'MV25', 'MV26', 'MV27', 'MV28', 'MV29', 'MV3', 'MV30', 'MV31', 'MV32', 'MV33', 'MV34', 'MV35', 'MV37', 'MV38', 'MV39', 'MV4', 'MV40', 'MV41', 'MV42', 'MV43', 'MV44', 'MV45', 'MV46', 'MV47', 'MV48', 'MV49', 'MV5', 'MV50', 'MV51', 'MV52', 'MV53', 'MV54', 'MV55', 'MV56', 'MV57', 'MV58', 'MV59', 'MV6', 'MV60', 'MV61', 'MV62', 'MV63', 'MV64', 'MV65', 'MV66', 'MV67', 'MV68', 'MV69', 'MV7', 'MV70', 'MV71', 'MV72', 'MV73', 'MV74', 'MV75', 'MV9', 'Q1', 'Q10', 'Q12', 'Q123', 'Q14', 'Q145', 'Q167', 'Q172', 'Q175', 'Q18', 'Q19', 'Q20', 'Q21', 'Q227', 'Q228', 'Q23', 'Q230', 'Q231', 'Q232', 'Q233', 'Q234', 'Q235', 'Q236', 'Q237', 'Q238', 'Q239', 'Q241', 'Q242', 'Q243', 'Q244', 'Q245', 'Q246', 'Q247', 'Q248', 'Q249', 'Q250', 'Q251', 'Q252', 'Q253', 'Q254', 'Q255', 'Q256', 'Q257', 'Q258', 'Q259', 'Q26', 'Q260', 'Q261', 'Q262', 'Q263', 'Q264', 'Q265', 'Q266', 'Q267', 'Q268', 'Q269', 'Q270', 'Q271', 'Q28', 'Q31', 'Q34', 'Q4', 'Q44', 'Q46', 'Q49', 'Q5', 'Q50', 'Q51', 'Q54', 'Q6', 'Q61', 'Q62', 'Q67', 'Q69', 'Q7', 'Q73', 'Q9', 'QT1', 'S4', 'S49', 'S6', 'S60', 'S65', 'S66', 'S67', 'S68', 'S69', 'S70', 'S71', 'S72', 'S73', 'S74', 'S75', 'S76', 'S77', 'S78', 'S79', 'S8', 'TL1', 'UV1510', 'UV1531', 'UV316', 'UV380', 'UV730', 'UV997', 'X1', 'Z1', 'Z15', 'Z18', 'Z31', 'Z33', 'Z34', 'Z4')
num_classes = len(class_name)
metainfo = dict(classes=class_name, palette=[(220, 20, 60)]*num_classes) # 这个是必须的，否则会造成loss均为0的情况

model = dict(
    type='DINO',
    num_queries=900,  # num_matching_queries
    with_box_refine=True,
    as_two_stage=True,
    data_preprocessor=dict(
        type='DetDataPreprocessor',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        bgr_to_rgb=True,
        pad_size_divisor=1),
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=False),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet50')),
    neck=dict(
        type='ChannelMapper',
        in_channels=[512, 1024, 2048],
        kernel_size=1,
        out_channels=256,
        act_cfg=None,
        norm_cfg=dict(type='GN', num_groups=32),
        num_outs=4),
    encoder=dict(
        num_layers=6,
        layer_cfg=dict(
            self_attn_cfg=dict(embed_dims=256, num_levels=4,
                               dropout=0.0),  # 0.1 for DeformDETR
            ffn_cfg=dict(
                embed_dims=256,
                feedforward_channels=2048,  # 1024 for DeformDETR
                ffn_drop=0.0))),  # 0.1 for DeformDETR
    decoder=dict(
        num_layers=6,
        return_intermediate=True,
        layer_cfg=dict(
            self_attn_cfg=dict(embed_dims=256, num_heads=8,
                               dropout=0.0),  # 0.1 for DeformDETR
            cross_attn_cfg=dict(embed_dims=256, num_levels=4,
                                dropout=0.0),  # 0.1 for DeformDETR
            ffn_cfg=dict(
                embed_dims=256,
                feedforward_channels=2048,  # 1024 for DeformDETR
                ffn_drop=0.0)),  # 0.1 for DeformDETR
        post_norm_cfg=None),
    positional_encoding=dict(
        num_feats=128,
        normalize=True,
        offset=0.0,  # -0.5 for DeformDETR
        temperature=20),  # 10000 for DeformDETR
    bbox_head=dict(
        type='DINOHead',
        num_classes=num_classes,  
        sync_cls_avg_factor=True,
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),  # 2.0 in DeformDETR
        loss_bbox=dict(type='L1Loss', loss_weight=5.0),
        loss_iou=dict(type='GIoULoss', loss_weight=2.0)),
    dn_cfg=dict(  # TODO: Move to model.train_cfg ?
        label_noise_scale=0.5,
        box_noise_scale=1.0,  # 0.4 for DN-DETR
        group_cfg=dict(dynamic=True, num_groups=None,
                       num_dn_queries=100)),  # TODO: half num_dn_queries
    # training and testing settings
    train_cfg=dict(
        assigner=dict(
            type='HungarianAssigner',
            match_costs=[
                dict(type='FocalLossCost', weight=2.0),
                dict(type='BBoxL1Cost', weight=5.0, box_format='xywh'),
                dict(type='IoUCost', iou_mode='giou', weight=2.0)
            ])),
    test_cfg=dict(max_per_img=300))  # 100 for DeformDETR

# train_pipeline, NOTE the img_scale and the Pad's size_divisor is different
# from the default setting in mmdet.
train_pipeline = [
    dict(type='LoadImageFromFile', backend_args={{_base_.backend_args}}),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='RandomChoice',
         transforms=[
            [
                dict(type='PhotoMetricDistortion', 
                      brightness_delta=int(0.1 * 255),
                      contrast_range=(0.8, 1.2),
                      saturation_range=(0.8, 1.2),
                      hue_delta=int(0.01 * 360)),
            ],
            [
                dict(
                    # 使用之前要pip install imagecorruptions albumentations
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
    dict(type='PackDetInputs')
]
test_pipeline = [
    dict(type='LoadImageFromFile', backend_args={{_base_.backend_args}}),
    dict(type='Resize', scale=(1333, 800), keep_ratio=True),
    # If you don't have a gt annotation, delete the pipeline
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor'))
]
# data_root='/home/star/8T/yyc/dataset/分离出来的数据集0616_10000/'
# dataset_10000=dict(
#     type='CocoDataset',
#     data_root=data_root,
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     backend_args={{_base_.backend_args}},
#     filter_cfg=dict(filter_empty_gt=False, min_size=32),
#     ann_file='annotations/train2017.json',
#     data_prefix=dict(img='images/'))
# dataset_420=dict(
#     type='CocoDataset',
#     data_root='/home/star/2T/yyc/cebaodengft0514_420',
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     backend_args={{_base_.backend_args}},
#     filter_cfg=dict(filter_empty_gt=False, min_size=32),
#     ann_file='annotations/train2017.json',
#     data_prefix=dict(img='images/'))
# dataset_pesudo_81955=dict(
#     type='CocoDataset',
#     data_root='/home/star/2T/outputs_pesudo_81955',
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     backend_args={{_base_.backend_args}},
#     filter_cfg=dict(filter_empty_gt=False, min_size=32),
#     ann_file='annotations/train2017.json',
#     data_prefix=dict(img='images/'))
# dataset_132_fzl50_danzhongchong=dict(
#     type='CocoDataset',
#     data_root='/home/star/2T/yyc/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs',
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     backend_args={{_base_.backend_args}},
#     filter_cfg=dict(filter_empty_gt=False, min_size=32),
#     ann_file='annotations/train2017.json',
#     data_prefix=dict(img='images/'))
# background_xiaochong200=dict(
#     type='CocoDataset',
#     data_root='/home/star/2T/yyc/背景图和分离出的小虫图/小虫背景训练集mmdet_dino',
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     backend_args={{_base_.backend_args}},
#     filter_cfg=dict(filter_empty_gt=False, min_size=32), # 是否过滤掉不包含 GT 的图片
#     ann_file='annotations/train2017.json',
#     data_prefix=dict(img='images/'))
# val_dataset=dict(
#     metainfo=metainfo,
#     type='CocoDataset',
#     data_root=data_root,
#     test_mode=True,
#     pipeline=test_pipeline,
#     ann_file='annotations/val2017.json',
#     data_prefix=dict(img='images/'))


# 2025年1021号用于实验的数据集
# dataset_singleclass=dict(
#     type='CocoDataset',
#     data_root='/home/star/2T-new/yyc/exp3_20251020/coco_annotations_insect',
#     metainfo=metainfo,
#     return_classes=True,
#     pipeline=train_pipeline,
#     backend_args={{_base_.backend_args}},
#     filter_cfg=dict(filter_empty_gt=False, min_size=32), # 是否过滤掉不包含 GT 的图片
#     ann_file='annotations/train2017.json',
#     data_prefix=dict(img='train2017/'))
# val_dataset_singleclass=dict(
#     metainfo=metainfo,
#     type='CocoDataset',
#     data_root='/home/star/2T-new/yyc/exp3_20251020/coco_annotations_insect',
#     test_mode=True,
#     pipeline=test_pipeline,
#     ann_file='annotations/val2017.json',
#     data_prefix=dict(img='val2017/'))
dataset_multiclass=dict(
    type='CocoDataset',
    data_root='/home/star/2T/yyc/exp3_20251020/12000multi_class_voc_dataset_split712_export4/coco',
    metainfo=metainfo,
    return_classes=True,
    pipeline=train_pipeline,
    backend_args={{_base_.backend_args}},
    filter_cfg=dict(filter_empty_gt=False, min_size=32), # 是否过滤掉不包含 GT 的图片
    ann_file='annotations/instances_train.json',
    data_prefix=dict(img='images/train/'))
val_dataset_multiclass=dict(
    metainfo=metainfo,
    type='CocoDataset',
    data_root='/home/star/2T/yyc/exp3_20251020/12000multi_class_voc_dataset_split712_export4/coco',
    test_mode=True,
    pipeline=test_pipeline,
    ann_file='annotations/instances_train.json',
    data_prefix=dict(img='images/train/'))


train_dataloader = dict(
    batch_size=2,  
    num_workers=4,  
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dataset_multiclass)  # 数据集选择
    # dataset=dict(type='ConcatDataset', datasets=[dataset_10000,dataset_420,dataset_pesudo_81955,dataset_132_fzl50_danzhongchong,background_xiaochong200]))
val_dataloader = dict(
    batch_size=2,  
    num_workers=4,  
    dataset=val_dataset_multiclass)  # 数据集选择
test_dataloader = val_dataloader
val_evaluator = dict(
        type='CocoMetric',
        ann_file='/home/star/2T/yyc/exp3_20251020/12000multi_class_voc_dataset_split712_export4/coco/annotations/instances_train.json',  # 这里不要忘记修改！
        metric='bbox',
        format_only=False, # 是否仅输出检测结果json文件，适用于没有标签数据集
        # outfile_prefix='./work_dirs/coco_detection/test'
        )
test_evaluator = val_evaluator

# optimizer
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(
        type='AdamW',
        lr=0.0001,  # 0.0002 for DeformDETR
        weight_decay=0.0001),
    clip_grad=dict(max_norm=0.1, norm_type=2),
    paramwise_cfg=dict(custom_keys={'backbone': dict(lr_mult=0.1)})
)  # custom_keys contains sampling_offsets and reference_points in DeformDETR  # noqa

# learning policy
max_epochs = 12
default_hooks = dict(
    checkpoint=dict(interval=1, max_keep_ckpts=2, save_best='auto'),
    logger=dict(type='LoggerHook', interval=10))
train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=max_epochs, val_interval=18)

val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

param_scheduler = [
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_epochs,
        by_epoch=True,
        milestones=[11],
        gamma=0.1)
]

# NOTE: `auto_scale_lr` is for automatically scaling LR,
# USER SHOULD NOT CHANGE ITS VALUES.
# base_batch_size = (8 GPUs) x (2 samples per GPU)
auto_scale_lr = dict(enable=True, base_batch_size=16)
