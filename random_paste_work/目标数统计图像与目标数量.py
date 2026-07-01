import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

# 定义路径
annotations_dir = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗/Annotations'
threshold = -1  # 可设置阈值

# 统计变量
total_target_count = 0
images_above_threshold_count = 0
remaining_target_count = 0

# 获取标注文件列表
annotation_files = [f for f in os.listdir(annotations_dir) if f.endswith('.xml')]

# 遍历标注文件并统计目标数
for annotation_file in tqdm(annotation_files, desc="Processing annotations"):
    tree = ET.parse(os.path.join(annotations_dir, annotation_file))
    root = tree.getroot()
    
    # 统计目标数
    objects = root.findall('object')
    object_count = len(objects)
    
    total_target_count += object_count
    
    if object_count > threshold:
        images_above_threshold_count += 1
    else:
        remaining_target_count += object_count

# 打印统计结果
print(f"Images with targets greater than {threshold}: {images_above_threshold_count}")
print(f"Total target count: {total_target_count}")
print(f"Remaining target count: {remaining_target_count}")
