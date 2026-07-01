import os
import random
import xml.etree.ElementTree as ET
import cv2
from PIL import Image, ImageDraw, ImageFont

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

# no labels
def draw_bounding_boxes_insect(image_path, xml_path, output_path, font_size=50): 
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
        draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=5) #小虫 5 大虫 10
        # # Draw the label
        # text_bbox = draw.textbbox((xmin, ymin), label, font=font)
        # text_width = text_bbox[2] - text_bbox[0]
        # text_height = text_bbox[3] - text_bbox[1]
        # text_background = [(xmin, (ymin - text_height)), ((xmin + text_width), ymin)]
        # draw.rectangle(text_background, fill="red")
        # draw.text((xmin, (ymin - text_height)), label, fill="white", font=font)

    # Save the resulting image
    image.save(output_path, quality=100)

def sample_and_draw(img_dir, xml_dir, output_dir, sample_size):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all image files
    img_files = [f for f in os.listdir(img_dir) if f.endswith(".jpg")]

    # Randomly sample the specified number of image files
    sampled_files = random.sample(img_files, sample_size)

    for img_file in sampled_files:
        img_path = os.path.join(img_dir, img_file)
        xml_path = os.path.join(xml_dir, img_file.replace('.jpg', '.xml'))
        output_path = os.path.join(output_dir, img_file)
        draw_bounding_boxes(img_path, xml_path, output_path)

# Define paths
img_dir = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/images'
xml_dir = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/xml'
output_dir = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/visualize'
sample_size = 20

# Sample and draw
# sample_and_draw(img_dir, xml_dir, output_dir, sample_size)

draw_bounding_boxes_insect('/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/0220715_Image_20220715100546085-3.jpg', 
                           '/home/yaoteam/yaoteam/yyc/random_paste_work/数据集/大小虫/xml/0220715_Image_20220715100546085-3.xml', 
                           '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/da_xiao_chong_biao_ji.jpg')


