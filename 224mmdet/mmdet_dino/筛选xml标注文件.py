import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def filter_bboxes(xml_file, width_threshold, height_threshold):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    objects_to_remove = []
    for obj in root.findall('object'):
        xmin = round(float(obj.find('bndbox/xmin').text))
        ymin = round(float(obj.find('bndbox/ymin').text))
        xmax = round(float(obj.find('bndbox/xmax').text))
        ymax = round(float(obj.find('bndbox/ymax').text))

        width = xmax - xmin
        height = ymax - ymin

        if width < width_threshold and height < height_threshold:
            objects_to_remove.append(obj)

    for obj in objects_to_remove:
        root.remove(obj)

    tree.write(xml_file)

def batch_filter_bboxes(xml_dir, width_threshold, height_threshold):
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    for xml_file in tqdm(xml_files):
        xml_file_path = os.path.join(xml_dir, xml_file)
        filter_bboxes(xml_file_path, width_threshold, height_threshold)

# 设置路径和阈值
xml_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件汇总'
width_threshold = 151
height_threshold = 151

# 批量处理XML文件
batch_filter_bboxes(xml_dir, width_threshold, height_threshold)
