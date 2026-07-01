import os
import xml.etree.ElementTree as ET
from PIL import Image

def create_voc_xml(image_path, xml_path):
    # 读取图片信息
    with Image.open(image_path) as img:
        width, height = img.size
        depth = len(img.getbands())

    # 创建 XML 文件的结构
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "filename").text = os.path.basename(image_path)
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    # 将 XML 写入文件
    tree = ET.ElementTree(annotation)
    tree.write(xml_path)

def create_xmls_for_directory(image_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历目录中的所有图片
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, filename)
            xml_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".xml")
            create_voc_xml(image_path, xml_path)

# 图片目录和输出目录
image_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/背景图和分离出的小虫图/小虫背景训练集mmdet_dino/images'  # 替换为您的图片目录路径
output_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/背景图和分离出的小虫图/小虫背景训练集mmdet_dino/xml'  # 替换为输出 XML 文件的目录路径

create_xmls_for_directory(image_dir, output_dir)
