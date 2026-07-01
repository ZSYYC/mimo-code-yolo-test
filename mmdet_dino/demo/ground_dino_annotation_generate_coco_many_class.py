import os
import json
from PIL import Image
import xml.etree.ElementTree as ET

# 类别映射字典
label_map = {}

def create_voc_xml(image_path, predictions, xml_path, confidence_threshold=0.5):
    # 根据图片格式自动打开图像
    with Image.open(image_path) as img:
        width, height = img.size
        depth = len(img.getbands())

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "filename").text = os.path.basename(image_path)
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    for label, score, bbox in zip(predictions['labels'], predictions['scores'], predictions['bboxes']):
        if score < confidence_threshold:
            continue
        object_tag = ET.SubElement(annotation, "object")
        ET.SubElement(object_tag, "name").text = label_map.get(label, "unknown")
        bndbox = ET.SubElement(object_tag, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(bbox[0])
        ET.SubElement(bndbox, "ymin").text = str(bbox[1])
        ET.SubElement(bndbox, "xmax").text = str(bbox[2])
        ET.SubElement(bndbox, "ymax").text = str(bbox[3])

    tree = ET.ElementTree(annotation)
    tree.write(xml_path)

def convert_predictions_to_voc(total_dir, output_dir, confidence_threshold=0.5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for subdir in os.listdir(total_dir):
        subdir_path = os.path.join(total_dir, subdir)
        if os.path.isdir(subdir_path):
            json_dir = os.path.join(subdir_path, 'preds')
            img_dir = os.path.join(subdir_path, 'vis')  # 假设图像在每个子文件夹的 'vis' 目录中
            label_map[0] = subdir  # 将子文件夹名作为类别名映射

            for json_file in os.listdir(json_dir):
                if json_file.endswith('.json'):
                    json_path = os.path.join(json_dir, json_file)
                    with open(json_path) as f:
                        predictions = json.load(f)
                    
                    # 获取图像文件的扩展名，并根据扩展名查找图像
                    base_name = os.path.splitext(json_file)[0]
                    image_path = os.path.join(img_dir, base_name)  # 不带扩展名
                    image_path = next((os.path.join(img_dir, base_name + ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp'] if os.path.exists(os.path.join(img_dir, base_name + ext))), None)
                    
                    if image_path:
                        xml_path = os.path.join(output_dir, json_file.replace('.json', '.xml'))
                        create_voc_xml(image_path, predictions, xml_path, confidence_threshold)

# 设置路径
total_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/mosquito_output'
output_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/mosquito_output_xml'
confidence_threshold = 0.25

convert_predictions_to_voc(total_dir, output_dir, confidence_threshold)
