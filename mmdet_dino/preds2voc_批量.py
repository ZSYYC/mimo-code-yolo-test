import json
import os
import xml.etree.ElementTree as ET
from PIL import Image
from tqdm import tqdm

# 此代码实现的功能是将某一目录的preds文件夹下的所有标注文件转换成voc格式输出，并将类别名都定为insect。现在新任务：要实现批量处理，现在给定2个目录,如下
# intput folder
# 	-class1
# 		--preds
# 			---xxx.json
# 	-class2
# 	-class3
# .....
# input img
# 	-class1
# 	              --xxx.jpg
# 	-class2
# 	-class3
# 将某一类别文件夹下的目标，其标签都为该类别文件夹名，结果xml文件都输出到同一目录即可

def create_voc_xml(image_path, predictions, xml_path, class_name, confidence_threshold=0.5):
    with Image.open(image_path) as img:
        width, height = img.size
        depth = len(img.getbands())

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "filename").text = os.path.basename(image_path)
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = str(depth)

    for score, bbox in zip(predictions['scores'], predictions['bboxes']):
        if score < confidence_threshold:
            continue
        object_tag = ET.SubElement(annotation, "object")
        ET.SubElement(object_tag, "name").text = class_name
        bndbox = ET.SubElement(object_tag, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(bbox[0])
        ET.SubElement(bndbox, "ymin").text = str(bbox[1])
        ET.SubElement(bndbox, "xmax").text = str(bbox[2])
        ET.SubElement(bndbox, "ymax").text = str(bbox[3])

    tree = ET.ElementTree(annotation)
    tree.write(xml_path)

def convert_predictions_to_voc(input_folder, input_img_folder, output_folder, confidence_threshold=0.5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)
        if not os.path.isdir(class_folder_path):
            continue
        
        preds_folder = os.path.join(class_folder_path, 'preds')
        if not os.path.exists(preds_folder):
            continue
        
        image_folder = os.path.join(input_img_folder, class_folder)
        if not os.path.exists(image_folder):
            continue
        
        class_output_folder = os.path.join(output_folder, class_folder)
        if not os.path.exists(class_output_folder):
            os.makedirs(class_output_folder)
        
        json_files = [f for f in os.listdir(preds_folder) if f.endswith('.json')]
        
        for json_file in tqdm(json_files, desc=f"Converting {class_folder} predictions"):
            json_path = os.path.join(preds_folder, json_file)
            with open(json_path) as f:
                predictions = json.load(f)
            
            image_path = os.path.join(image_folder, json_file.replace('.json', '.jpg'))
            xml_path = os.path.join(class_output_folder, json_file.replace('.json', '.xml'))
            
            create_voc_xml(image_path, predictions, xml_path, class_folder, confidence_threshold)

# 设置路径
input_folder = '/home/yaoteam/yaoteam/wz/测试/insects/preds'
input_img_folder = '/home/yaoteam/yaoteam/wz/测试/10000张大虫抽样10张'
output_folder = '/home/yaoteam/yaoteam/wz/测试/'
confidence_threshold = 0.3

convert_predictions_to_voc(input_folder, input_img_folder, output_folder, confidence_threshold)
