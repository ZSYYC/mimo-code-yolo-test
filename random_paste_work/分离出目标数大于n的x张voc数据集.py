import os
import random
import shutil
import xml.etree.ElementTree as ET
from tqdm import tqdm

# 定义路径
images_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images'
annotations_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/xml汇总'
output_images_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/论文数据集展示用500/images'
output_annotations_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/论文数据集展示用500/xml'

# 确保输出文件夹存在
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_annotations_dir, exist_ok=True)

# 获取标注文件列表
annotation_files = [f for f in os.listdir(annotations_dir) if f.endswith('.xml')]

# 筛选目标数大于5的图片和标注文件
selected_files = []
threshold = 6

for annotation_file in tqdm(annotation_files, desc="Filtering annotations"):
    tree = ET.parse(os.path.join(annotations_dir, annotation_file))
    root = tree.getroot()
    
    objects = root.findall('object')
    if len(objects) > threshold:
        file_id = annotation_file.split('.')[0]
        selected_files.append(file_id)

# 随机选择500个文件
# selected_files = random.sample(selected_files, min(len(selected_files), 500))

# 复制选定的图片和标注文件
for file_id in tqdm(selected_files, desc="Copying files"):
    img_src_path = os.path.join(images_dir, file_id + '.jpg')
    img_dest_path = os.path.join(output_images_dir, file_id + '.jpg')
    xml_src_path = os.path.join(annotations_dir, file_id + '.xml')
    xml_dest_path = os.path.join(output_annotations_dir, file_id + '.xml')
    
    shutil.copy(img_src_path, img_dest_path)
    shutil.copy(xml_src_path, xml_dest_path)

print(f"Copied {len(selected_files)} images and their annotations to the specified folder.")
