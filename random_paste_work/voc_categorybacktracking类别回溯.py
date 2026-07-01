# 任务：现在有一系列从voc数据集裁剪下来的小图分类数据集，有一一对应关系，可以由以下函数检查其唯一对应关系：
# def check_voc_labels(voc_folder_path, cropped_images_folder):
#     # 存储每个xml文件中的所有框
#     voc_bboxes = {}
#     cropped_images_num=0
#     voc_cropped_images_num=0
#     # 遍历VOC标注文件夹
#     for filename in os.listdir(voc_folder_path):
#         if not filename.endswith('.xml'):
#             continue     
#         file_path = os.path.join(voc_folder_path, filename)
#         tree = ET.parse(file_path)
#         root = tree.getroot()      
#         # 获取文件中的所有框
#         boxes = []
#         for obj in root.findall('object'):
#             bndbox = obj.find('bndbox')
#             x1 = int(bndbox.find('xmin').text)
#             y1 = int(bndbox.find('ymin').text)
#             x2 = int(bndbox.find('xmax').text)
#             y2 = int(bndbox.find('ymax').text)
#             boxes.append((x1, y1, x2, y2))
#             voc_cropped_images_num+=1
#         voc_bboxes[filename[:-4]] = boxes   
#     # print(voc_bboxes['Image_20020101001946509'])
#     # 检查分类后的小图文件夹
#     for class_name in tqdm(os.listdir(cropped_images_folder), desc="Processing classes"):
#         class_folder = os.path.join(cropped_images_folder, class_name)
#         if not os.path.isdir(class_folder):
#             continue     
#         for image_file in os.listdir(class_folder):
#             if not image_file.endswith('.jpg'):
#                 continue          
#             parts = image_file[:-4].split('_')
#             xml_base_name = '_'.join(parts[:-4])
#             x1, y1, x2, y2 = map(int, parts[-4:])
#             if xml_base_name not in voc_bboxes:
#                 # print(f"XML file not found: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}") # 允许小图是所有的，voc数据集只是其中部分的所以允许xml文件找不到
#                 continue        
#             matched = False
#             # print(f'开始寻找{image_file}的对应匹配')
#             for box in voc_bboxes[xml_base_name]:
#                 bx1, by1, bx2, by2 = box           
#                 # print(f"Checking box: {box} in {xml_base_name}.xml against {x1, y1, x2, y2}")
#                 if (abs(bx1 - x1) <= 2 and abs(by1 - y1) <= 2 and abs(bx2 - x2) <= 2 and abs(by2 - y2) <= 2):
#                     matched = True
#                     cropped_images_num+=1
#                     voc_bboxes[xml_base_name].remove(box)
#                     break         
#             if not matched:
#                 print(f"Bounding box {x1},{y1},{x2},{y2} not found in XML file: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}")
#             # break
#     print('**************************打印在小图中没有的框**************************')
#     # 打印在小图中没有的框
#     for xml_base_name, boxes in voc_bboxes.items():
#         if boxes:
#             for box in boxes:
#                 print(f"Bounding box {box[0]},{box[1]},{box[2]},{box[3]} in XML file: {xml_base_name}.xml not found in any cropped images")
#     print(f'all_voc_cropped_images_num：{voc_cropped_images_num},matched_voc_bboxes_cropped_images_num:{cropped_images_num}')
# # 使用示例 
# voc_folder_path = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/train_dataset/test/annotations'
# cropped_images_folder = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/crop_img' # 定位在图片的上一级目录！
# check_voc_labels(voc_folder_path, cropped_images_folder)
# 如果得到了all_voc_cropped_images_num：47387,matched_voc_bboxes_cropped_images_num:47387，即两者数量相同，匹配成功。现在要用python实现更新voc数据集上每一个框的类别，根据与其对应小图所在的类别来更新。
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm


def integerize_coordinates(xml_folder_path):
    # 遍历文件夹中的每个XML文件
    for filename in os.listdir(xml_folder_path):
        if not filename.endswith('.xml'):
            continue

        file_path = os.path.join(xml_folder_path, filename)

        # 解析XML文件
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 遍历每个object标签
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')

            # 获取并整数化坐标
            x1 = round(float(bndbox.find('xmin').text))
            y1 = round(float(bndbox.find('ymin').text))
            x2 = round(float(bndbox.find('xmax').text))
            y2 = round(float(bndbox.find('ymax').text))

            # 更新XML中的坐标
            bndbox.find('xmin').text = str(x1)
            bndbox.find('ymin').text = str(y1)
            bndbox.find('xmax').text = str(x2)
            bndbox.find('ymax').text = str(y2)

        # 保存更新后的XML文件
        tree.write(file_path)

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
                print(f"XML file not found: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}")
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
                pass
                print(f"Bounding box {x1},{y1},{x2},{y2} not found in XML file: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}")

            # break
    print('**************************打印在小图中没有的框**************************')
    # 打印在小图中没有的框
    for xml_base_name, boxes in voc_bboxes.items():
        if boxes:
            for box in boxes:
                print(f"Bounding box {box[0]},{box[1]},{box[2]},{box[3]} in XML file: {xml_base_name}.xml not found in any cropped images")

    print(f'all_voc_cropped_images_num：{voc_cropped_images_num},matched_voc_bboxes_cropped_images_num:{cropped_images_num}')
    return voc_cropped_images_num, cropped_images_num

def update_voc_labels_with_class(voc_folder_path, cropped_images_folder):
    # 存储每个xml文件中的所有框
    voc_bboxes = {}

    # 遍历VOC标注文件夹，解析XML并获取所有框
    for filename in os.listdir(voc_folder_path):
        if not filename.endswith('.xml'):
            continue
        
        file_path = os.path.join(voc_folder_path, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()

        boxes = []
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            x1 = int(bndbox.find('xmin').text)
            y1 = int(bndbox.find('ymin').text)
            x2 = int(bndbox.find('xmax').text)
            y2 = int(bndbox.find('ymax').text)
            boxes.append({'box': (x1, y1, x2, y2), 'element': obj})
        
        voc_bboxes[filename[:-4]] = {'file_path': file_path, 'boxes': boxes, 'tree': tree}

    # 遍历分类后的小图文件夹，更新对应的VOC框类别
    for class_name in tqdm(os.listdir(cropped_images_folder), desc="Processing classes"):
        class_folder = os.path.join(cropped_images_folder, class_name)
        if not os.path.isdir(class_folder):
            continue
        
        for image_file in os.listdir(class_folder):
            if not image_file.endswith('.jpg'):
                continue
            
            # 从小图的文件名提取信息
            parts = image_file[:-4].split('_')
            xml_base_name = '_'.join(parts[:-4])
            x1, y1, x2, y2 = map(int, parts[-4:])

            if xml_base_name not in voc_bboxes:
                # 如果XML文件不存在，跳过
                continue

            # 匹配边界框
            matched = False
            for box_info in voc_bboxes[xml_base_name]['boxes']:
                bx1, by1, bx2, by2 = box_info['box']
                
                if (abs(bx1 - x1) <= 2 and abs(by1 - y1) <= 2 and abs(bx2 - x2) <= 2 and abs(by2 - y2) <= 2):
                    matched = True
                    
                    # 更新VOC文件中object的类别
                    obj_element = box_info['element']
                    obj_element.find('name').text = class_name
                    break

            if not matched:
                pass
                # print(f"Bounding box {x1},{y1},{x2},{y2} not found in XML file: {xml_base_name}.xml for image {os.path.join(class_name, image_file)}")
    
    # 保存更新后的VOC文件
    for xml_base_name, voc_info in voc_bboxes.items():
        voc_info['tree'].write(voc_info['file_path'])
        # print(f"Updated and saved: {voc_info['file_path']}")

# 使用示例 
# voc_folder_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/xml'
# cropped_images_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/2024summer_biaozhu_small_img_12000' # 定位在图片的上一级目录！
voc_folder_path = '/home/yaoteam/yaoteam/wz/12000图片及其对应xml/UpdatedAnnotations/'
cropped_images_folder = '/home/yaoteam/yaoteam/wz/12000_小虫多分类图片_修改/' # 定位在图片的上一级目录！


# voc_folder_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/xml汇总20250225'
# cropped_images_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/crop_img' # 定位在图片的上一级目录！
# voc_folder_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/xml'
# cropped_images_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/crop_img_2000_checked' # 定位在图片的上一级目录！

# integerize_coordinates(voc_folder_path)
all_voc_cropped_images_num, matched_voc_bboxes_cropped_images_num = check_voc_labels(voc_folder_path, cropped_images_folder)
print(f'{all_voc_cropped_images_num = }')
print(f'{matched_voc_bboxes_cropped_images_num = }')

update_voc_labels_with_class(voc_folder_path, cropped_images_folder)
# if all_voc_cropped_images_num == matched_voc_bboxes_cropped_images_num:
#     update_voc_labels_with_class(voc_folder_path, cropped_images_folder)
# else:
#     print('没有一一匹配成功，跳过更新！！！！')
