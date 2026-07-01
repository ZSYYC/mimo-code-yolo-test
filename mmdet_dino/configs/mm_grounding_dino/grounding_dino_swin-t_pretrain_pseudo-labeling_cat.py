_base_ = 'grounding_dino_swin-t_pretrain_obj365.py'

test_pipeline = [
    dict(
        type='LoadImageFromFile', backend_args=None,
        imdecode_backend='pillow'),
    dict(
        type='FixScaleResize',
        scale=(800, 1333),
        keep_ratio=True,
        backend='pillow'),
    dict(type='LoadTextAnnotations'),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'text', 'custom_entities',
                   'tokens_positive'))
]

data_root = 'data/img_cebaodeng_pseudo/'

val_dataloader = dict(
    batch_size=8,
    num_workers=8,
    persistent_workers=False,
    dataset=dict(
        type='ODVGDataset',
        data_root=data_root,
        label_map_file='insect_label_map.json',
        ann_file='insect_train_od.json',
        data_prefix=dict(img='images/'),
        pipeline=test_pipeline,
        return_classes=True))
test_dataloader = val_dataloader

val_evaluator = dict(
    _delete_=True,
    outfile_path=data_root + 'insect_train_od_v1.json',
    img_prefix=data_root + 'images/',
    score_thr=0.5, # 0.4
    nms_thr=0.5,
    type='DumpODVGResults')
test_evaluator = val_evaluator
