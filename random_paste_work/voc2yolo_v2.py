import os
import xml.etree.ElementTree as ET
import random
import shutil
from PIL import Image

def parse_voc_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    objects = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        objects.append((name, xmin, ymin, xmax, ymax))
    return objects

def convert_to_yolo(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotations(xml_dir, yolo_dir, image_dir):
    classes = {}
    for xml_file in os.listdir(xml_dir):
        if not xml_file.endswith('.xml'):
            continue
        xml_path = os.path.join(xml_dir, xml_file)
        objects = parse_voc_xml(xml_path)
        txt_file = os.path.splitext(xml_file)[0] + '.txt'
        with open(os.path.join(yolo_dir, txt_file), 'w') as out_file:
            for obj in objects:
                cls_name, xmin, ymin, xmax, ymax = obj
                if cls_name not in classes:
                    classes[cls_name] = len(classes)
                cls_id = classes[cls_name]
                # Supporting multiple image formats (JPG, BMP)
                img_file = os.path.splitext(xml_file)[0]
                for ext in ['.jpg', '.bmp']:
                    img_path = os.path.join(image_dir, img_file + ext)
                    if os.path.exists(img_path):
                        break
                img_size = Image.open(img_path).size
                yolo_box = convert_to_yolo(img_size, (xmin, xmax, ymin, ymax))
                out_file.write(f"{cls_id} {' '.join(map(str, yolo_box))}\n")
    return classes

def split_dataset(image_dir, label_dir, output_dir, split_ratio=(0.7, 0.1, 0.2)):
    images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.bmp'))]
    random.shuffle(images)
    train_split = int(len(images) * split_ratio[0])
    val_split = train_split + int(len(images) * split_ratio[1])
    train_images = images[:train_split]
    val_images = images[train_split:val_split]
    test_images = images[val_split:]

    def copy_files(images, split_dir):
        for img in images:
            base_name = os.path.splitext(img)[0]
            shutil.copy(os.path.join(image_dir, img), os.path.join(output_dir, split_dir, 'images', img))
            shutil.copy(os.path.join(label_dir, base_name + '.txt'), os.path.join(output_dir, split_dir, 'labels', base_name + '.txt'))

    os.makedirs(os.path.join(output_dir, 'train/images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train/labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val/images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val/labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test/images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test/labels'), exist_ok=True)

    copy_files(train_images, 'train')
    copy_files(val_images, 'val')
    copy_files(test_images, 'test')

def generate_yaml(classes, output_dir):
    with open(os.path.join(output_dir, 'data.yaml'), 'w') as yaml_file:
        yaml_file.write('train: ./train/images\n')
        yaml_file.write('val: ./val/images\n')
        yaml_file.write('test: ./test/images\n')
        yaml_file.write('nc: {}\n'.format(len(classes)))
        yaml_file.write('names: {}\n'.format(list(classes.keys())))

xml_dir = '/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/few_xml'
yolo_dir = '/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/dataset_with_few_class/yolo_dataset_convert'
os.makedirs(yolo_dir, exist_ok=True)
image_dir = '/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/img'
output_dir = '/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/dataset_with_few_class'

classes = convert_annotations(xml_dir, yolo_dir, image_dir)
split_dataset(image_dir, yolo_dir, output_dir)
generate_yaml(classes, output_dir)