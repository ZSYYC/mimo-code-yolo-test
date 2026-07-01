import json
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
import random
from PIL import Image, ImageDraw, ImageFont

# 类别映射字典
label_map = {
    0: '灰飞虱',
    # 1: 'class2',
    # 更多类别映射
}

def draw_bounding_boxes(image_path, xml_path, output_path, font_size=50):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    # Load a font
    font_path = "/home/yaoteam/yaoteam/yyc/wqy-microhei.ttc"  # 你可以根据需要更改字体路径
    font = ImageFont.truetype(font_path, font_size)
    # Parse the XML annotation file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(float(bbox.find('xmin').text))
        ymin = int(float(bbox.find('ymin').text))
        xmax = int(float(bbox.find('xmax').text))
        ymax = int(float(bbox.find('ymax').text))
        label = obj.find('name').text
        # Draw the bounding box
        draw.rectangle([xmin, ymin, xmax, ymax], outline="blue", width=5)
        # Draw the label
        text_bbox = draw.textbbox((xmin, ymin), label, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_background = [(xmin, (ymin - text_height)), ((xmin + text_width), ymin)]
        draw.rectangle(text_background, fill="red")
        draw.text((xmin, (ymin - text_height)), label, fill="white", font=font)

    # Save the resulting image
    image.save(output_path, quality=100)

def sample_and_draw(img_dir, xml_dir, output_dir, sample_size):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all image files
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith(".xml")]

    # Randomly sample the specified number of image files
    sampled_files = random.sample(xml_files, sample_size)

    for xml_file in sampled_files:
        img_path = os.path.join(img_dir, xml_file.replace('.xml', '.jpg'))
        xml_path = os.path.join(xml_dir, xml_file)
        output_path = os.path.join(output_dir, xml_file.replace('.xml', '.jpg'))
        draw_bounding_boxes(img_path, xml_path, output_path)

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

    tree.write(xml_file, encoding="utf-8", xml_declaration=True)

def filter_bboxes_feishi(xml_file):
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
        areas = width * height
        aspect_ratio = height / width
        if width < 30 or width > 200:
            objects_to_remove.append(obj)
            continue
        if height < 30 or height > 200:
            objects_to_remove.append(obj)
            continue
        if areas < 3000 or areas > 30000 :
            objects_to_remove.append(obj)
            continue
        if aspect_ratio < 0.34 or aspect_ratio > 3.0 :
            objects_to_remove.append(obj)
            continue

    for obj in objects_to_remove:
        root.remove(obj)

    tree.write(xml_file, encoding="utf-8", xml_declaration=True)

def batch_filter_bboxes(xml_dir, width_threshold, height_threshold):
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    for xml_file in tqdm(xml_files):
        xml_file_path = os.path.join(xml_dir, xml_file)
        filter_bboxes(xml_file_path, width_threshold, height_threshold)

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
        ET.SubElement(object_tag, "name").text = label_map.get(label, "unknown")
        bndbox = ET.SubElement(object_tag, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(bbox[0])
        ET.SubElement(bndbox, "ymin").text = str(bbox[1])
        ET.SubElement(bndbox, "xmax").text = str(bbox[2])
        ET.SubElement(bndbox, "ymax").text = str(bbox[3])

    tree = ET.ElementTree(annotation)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

def batch_filter_bboxes_feishi(xml_dir):
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    for xml_file in tqdm(xml_files):
        xml_file_path = os.path.join(xml_dir, xml_file)
        filter_bboxes_feishi(xml_file_path)    


def convert_predictions_to_voc(json_dir, img_dir, output_dir, confidence_threshold=0.3):
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
json_dir = '/home/yaoteam/yaoteam/wz/mvs-photo/灰飞虱/preds/'
img_dir = '/home/yaoteam/yaoteam/wz/mvs-photo/灰飞虱/'
output_dir = '/home/yaoteam/yaoteam/wz/mvs-photo/灰飞虱/xml'
confidence_threshold = 0.3 # 0.36
# json -》 VOC
convert_predictions_to_voc(json_dir, img_dir, output_dir, confidence_threshold)
print('convert_predictions_to_voc is done!')

#筛选xml标注框
# 设置路径和阈值

xml_dir = output_dir
# # width_threshold = 121
# # height_threshold = 121
# # # 批量处理XML文件
# # batch_filter_bboxes(xml_dir, width_threshold, height_threshold)
# # print('batch_filter_bboxes is done!')


# # 筛选xml标注框， 针对飞虱该如何制定 ？
# # 正则化
# batch_filter_bboxes_feishi(xml_dir)
# print('batch_filter_bboxes_feishi is done!')


# #抽样可视化
# # img_dir = ''
# # xml_dir = ''
# vis_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/vis_small_target'
# sample_size = 10

# # Sample and draw
# sample_and_draw(img_dir, xml_dir, vis_dir, sample_size)
# print('sample_and_draw is done!')