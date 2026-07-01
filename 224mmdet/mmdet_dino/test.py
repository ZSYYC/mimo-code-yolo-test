
# --- 必须放在脚本最前 ---
from mmdet.datasets import transforms as mmdet_transforms
from mmpretrain.datasets import transforms as mmpretrain_transforms
import mmpretrain.datasets
from mmdet.apis import init_detector
from mmpretrain import ImageClassificationInferencer
from mmengine import Config

print('✅ 环境检测：')
print('mmdet + mmpretrain registry 正常导入！')

det_config = 'configs/mm_grounding_dino/grounding_dino_swin-t_finetune_8xb4_20e_cat.py'
cls_config = '/home/star/8T/wz/小虫分类模型2021_17种_平衡_model_status/swin-base-wz.py'

model = init_detector(det_config, 'mmdet_dino_10420_20240722_swint_30_amp/best_coco_bbox_mAP_epoch_27.pth', device='cuda:1')
classifier = ImageClassificationInferencer(cls_config, pretrained=True)
print('✅ 模型初始化成功')