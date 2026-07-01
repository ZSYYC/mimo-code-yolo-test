import json
import xml.etree.ElementTree as ET
import os

def convert_odvg_to_voc(odvg_data, output_dir,min_score):
    # 解析JSON数据
    filename = odvg_data["filename"]
    height = odvg_data["height"]
    width = odvg_data["width"]
    detections = odvg_data["detection"]["instances"]
    
    # 创建XML根元素
    root = ET.Element("annotation")

    # 添加图像信息
    filename_elem = ET.SubElement(root, "filename")
    filename_elem.text = filename

    size_elem = ET.SubElement(root, "size")
    width_elem = ET.SubElement(size_elem, "width")
    width_elem.text = str(width)
    height_elem = ET.SubElement(size_elem, "height")
    height_elem.text = str(height)

    # 添加检测框信息
    for instance in detections:
        score = instance["score"]
        if score >= min_score:
            bbox = instance["bbox"]
            xmin, ymin, xmax, ymax = map(str, bbox)
            label = instance["label"]
            category = instance["category"]

            object_elem = ET.SubElement(root, "object")
            name_elem = ET.SubElement(object_elem, "name")
            name_elem.text = category
            pose_elem = ET.SubElement(object_elem, "pose")
            pose_elem.text = "Unspecified"
            truncated_elem = ET.SubElement(object_elem, "truncated")
            truncated_elem.text = "0"
            difficult_elem = ET.SubElement(object_elem, "difficult")
            difficult_elem.text = "0"

            bbox_elem = ET.SubElement(object_elem, "bndbox")
            xmin_elem = ET.SubElement(bbox_elem, "xmin")
            xmin_elem.text = xmin
            ymin_elem = ET.SubElement(bbox_elem, "ymin")
            ymin_elem.text = ymin
            xmax_elem = ET.SubElement(bbox_elem, "xmax")
            xmax_elem.text = xmax
            ymax_elem = ET.SubElement(bbox_elem, "ymax")
            ymax_elem.text = ymax

    # 创建XML树并保存到文件
    tree = ET.ElementTree(root)
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".xml")
    tree.write(output_path)

# 从JSON文件中读取多个ODVG数据
def process_json_file(json_file, output_dir, min_score=0.4):
    with open(json_file, 'r') as f:
        for line in f:
            odvg_data = json.loads(line)
            convert_odvg_to_voc(odvg_data, output_dir, min_score)

# 示例JSON文件和输出目录
json_file = "/home/yaoteam/yaoteam/yyc/mmdet_dino/data/val_img_cebaodeng/insect_train_od_v1.json"
output_directory = "/home/yaoteam/yaoteam/yyc/mmdet_dino/data/val_img_cebaodeng/output_xml"

# 创建输出目录（如果不存在）
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 处理JSON文件并转换为VOC格式的XML文件
process_json_file(json_file, output_directory,min_score=0.4)
