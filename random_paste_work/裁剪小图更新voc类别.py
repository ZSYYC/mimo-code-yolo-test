# 新任务：首先我根据voc标注文件，将目标裁剪成小图，接着我人工分类了这些小图，整理成imagenet分类模型训练集的格式，、
# 即对应类别的小图放置在对应类别的子文件夹目录里。子文件夹目录即类别名。
# 小图的命名规则为dst_file = os.path.join(target, os.path.basename(xml_file)[:-4] + f'_{x1}_{y1}_{x2}_{y2}.jpg')；
# 注意xml_file中也可能出现数字以及_符号，x1y1x2y2一定为int类型数字。 
# 要求给定voc标注文件夹路径和分类后小图文件夹路径，通过子文件夹名、小图文件名更新对应voc标注文件里面的类别。
# 如果小图在voc标注文件里找不到完全对应的框，则跳过这张小图同时打印出该小图所在的子目录以及该小图的文件名。
# 使用python完成应该有进度条提示。

import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def update_voc_labels(voc_folder_path, cropped_images_folder):
    # 遍历分类后的小图文件夹
    for class_name in tqdm(os.listdir(cropped_images_folder), desc="Processing classes"):
        class_folder = os.path.join(cropped_images_folder, class_name)
        if not os.path.isdir(class_folder):
            continue
        
        # 遍历每个类别文件夹中的小图
        for image_file in os.listdir(class_folder):
            if not image_file.endswith('.jpg'):
                continue
            
            # 从文件名解析出信息
            parts = image_file[:-4].split('_')
            xml_base_name = '_'.join(parts[:-4])
            x1, y1, x2, y2 = map(int, parts[-4:])
            
            # 查找对应的VOC标注文件
            xml_file = os.path.join(voc_folder_path, xml_base_name + '.xml')
            if not os.path.exists(xml_file):
                print(f"XML file not found: {xml_file}")
                continue
            
            # 解析XML文件
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # 查找对应的object标签
            matched = False
            for obj in root.findall('object'):
                bndbox = obj.find('bndbox')
                bx1 = int(bndbox.find('xmin').text)
                by1 = int(bndbox.find('ymin').text)
                bx2 = int(bndbox.find('xmax').text)
                by2 = int(bndbox.find('ymax').text)
                
                if bx1 == x1 and by1 == y1 and bx2 == x2 and by2 == y2:
                    obj.find('name').text = class_name
                    matched = True
                    break
            
            if matched:
                # 保存更新后的XML文件
                tree.write(xml_file)
            else:
                print(f"Bounding box not found: {os.path.join(class_name, image_file)}")

# 使用示例  配合 voc标签整数化代码、crop2smallimg、voc小图关联关系.py 来使用 待验证
voc_folder_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/outputs_cebaodeng1286/xml'
cropped_images_folder = 'path/to/your/cropped/images'
update_voc_labels(voc_folder_path, cropped_images_folder)
