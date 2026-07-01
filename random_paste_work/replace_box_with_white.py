import os
import cv2
import xml.etree.ElementTree as ET

def cover_boxes_with_white(image_folder, xml_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取所有 XML 文件
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    
    for xml_file in xml_files:
        # 解析 XML 文件
        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 获取对应的图像文件名（去掉 .xml 后缀）
        image_file = xml_file.replace('.xml', '.jpg')  # 假设图片是 JPG 格式
        image_path = os.path.join(image_folder, image_file)
        
        # 读取图像
        image = cv2.imread(image_path)
        
        # 遍历 XML 中的所有目标框
        for obj in root.findall('object'):
            # 获取目标框的坐标
            bbox = obj.find('bndbox')
            x_min = int(bbox.find('xmin').text)
            y_min = int(bbox.find('ymin').text)
            x_max = int(bbox.find('xmax').text)
            y_max = int(bbox.find('ymax').text)
            
            # 用白色矩形覆盖目标框
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 255, 255), thickness=cv2.FILLED)

        # 保存处理后的图像
        output_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_path, image)

        print(f"Processed {image_file}, saved to {output_folder}")

# 示例使用
image_folder = '/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/images'  # 替换为您的图片文件夹路径
xml_folder = '/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/xml_insect'       # 替换为您的 XML 文件夹路径
output_folder = '/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/output_white'        # 替换为输出文件夹路径

cover_boxes_with_white(image_folder, xml_folder, output_folder)
