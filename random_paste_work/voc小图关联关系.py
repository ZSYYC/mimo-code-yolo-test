import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def check_voc_labels(voc_folder_path, cropped_images_folder):
    # 存储每个xml文件中的所有框
    voc_bboxes = {}
    cropped_images_num=0
    voc_cropped_images_num=0
    # 遍历VOC标注文件夹
    for filename in os.listdir(voc_folder_path):
        if not filename.endswith('.xml'):
            continue
        
        file_path = os.path.join(voc_folder_path, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 获取文件中的所有框
        boxes = []
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            x1 = int(bndbox.find('xmin').text)
            y1 = int(bndbox.find('ymin').text)
            x2 = int(bndbox.find('xmax').text)
            y2 = int(bndbox.find('ymax').text)
            boxes.append((x1, y1, x2, y2))
            voc_cropped_images_num+=1
        voc_bboxes[filename[:-4]] = boxes
    
    # print(voc_bboxes['Image_20020101001946509'])
    # 检查分类后的小图文件夹
    for class_name in tqdm(os.listdir(cropped_images_folder), desc="Processing classes"):
        class_folder = os.path.join(cropped_images_folder, class_name)
        if not os.path.isdir(class_folder):
            continue
        
        for image_file in os.listdir(class_folder):
            if not image_file.endswith('.jpg'):
                continue
            
            parts = image_file[:-4].split('_')
            xml_base_name = '_'.join(parts[:-4])
            x1, y1, x2, y2 = map(int, parts[-4:])
            
            # if xml_base_name != 'Image_20020101001946509' or x1!=3821:
            #     continue

            if xml_base_name not in voc_bboxes:
                # print(f"XML file not found: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}")
                continue
            
            matched = False
            # print(f'开始寻找{image_file}的对应匹配')
            for box in voc_bboxes[xml_base_name]:
                bx1, by1, bx2, by2 = box
                
                # print(f"Checking box: {box} in {xml_base_name}.xml against {x1, y1, x2, y2}")
                if (abs(bx1 - x1) <= 2 and abs(by1 - y1) <= 2 and abs(bx2 - x2) <= 2 and abs(by2 - y2) <= 2):
                    matched = True
                    cropped_images_num+=1
                    voc_bboxes[xml_base_name].remove(box)
                    break
            
            if not matched:
                print(f"Bounding box {x1},{y1},{x2},{y2} not found in XML file: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}")

            # break
    print('**************************打印在小图中没有的框**************************')
    # 打印在小图中没有的框
    for xml_base_name, boxes in voc_bboxes.items():
        if boxes:
            for box in boxes:
                print(f"Bounding box {box[0]},{box[1]},{box[2]},{box[3]} in XML file: {xml_base_name}.xml not found in any cropped images")

    print(f'all_voc_cropped_images_num：{voc_cropped_images_num},matched_voc_bboxes_cropped_images_num:{cropped_images_num}')


# 使用示例 ！！最好不要先使用cropv2进行像素裁剪再使用jpg转png。凡是使用该手段裁剪保存的图片均失去了一一对应的关系。
voc_folder_path = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/train_dataset/test/annotations'
cropped_images_folder = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/crop_img' # 定位在图片的上一级目录！
# voc_folder_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/outputs_pesudo_81955/xml'
# cropped_images_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/outputs_pesudo_81955/crop_img' # 定位在图片的上一级目录！
check_voc_labels(voc_folder_path, cropped_images_folder)

# Bounding box 3252,2101,3603,2271 in XML file: Image_20020101005950325.xml not found in any cropped images
# Bounding box 2459,2620,2652,2814 in XML file: 104488_16-04-22-03-49-49_1.xml not found in any cropped images
# Bounding box 2179,1129,2652,1624 in XML file: 3_23-07-10-07-17-39_0_b9bfb-2.xml not found in any cropped images
# Bounding box 1565,763,1766,1040 in XML file: 2906.xml not found in any cropped images
# Bounding box 2134,1625,2425,1886 in XML file: 105392_16-09-02-03-59-43_1.xml not found in any cropped images
# Bounding box 2593,1492,2829,1724 in XML file: Image_20020101012107120.xml not found in any cropped images
# Bounding box 211,633,661,1218 in XML file: 105392_16-07-03-21-08-38_2.xml not found in any cropped images
# voc_cropped_images_num：553347,cropped_images_num:553340
