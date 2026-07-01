import json
import os
import xml.etree.ElementTree as ET
from PIL import Image
from tqdm import tqdm

def create_voc_xml(image_path, predictions, xml_path, confidence_threshold=0.5):
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
        ET.SubElement(object_tag, "name").text = 'insect'
        bndbox = ET.SubElement(object_tag, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(bbox[0])
        ET.SubElement(bndbox, "ymin").text = str(bbox[1])
        ET.SubElement(bndbox, "xmax").text = str(bbox[2])
        ET.SubElement(bndbox, "ymax").text = str(bbox[3])

    tree = ET.ElementTree(annotation)
    tree.write(xml_path)

def convert_predictions_to_voc(json_dir, img_dir, output_dir, confidence_threshold=0.5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    for json_file in tqdm(json_files, desc="Converting predictions"):
        json_path = os.path.join(json_dir, json_file)
        with open(json_path) as f:
            predictions = json.load(f)
        
        image_path = os.path.join(img_dir, json_file.replace('.json', '.jpg'))
        xml_path = os.path.join(output_dir, json_file.replace('.json', '.xml'))
        
        create_voc_xml(image_path, predictions, xml_path, confidence_threshold)

# 设置路径
json_dir = '/home/yaoteam/yaoteam/wz/测试/抽样图片检测结果/preds'
img_dir = '/home/yaoteam/yaoteam/wz/groundingdino图片/'
output_dir = '/home/yaoteam/yaoteam/wz/1020groundingdino结果xml/'
confidence_threshold = 0.3

convert_predictions_to_voc(json_dir, img_dir, output_dir, confidence_threshold)
