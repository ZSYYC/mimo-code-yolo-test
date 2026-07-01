import os
import xml.etree.ElementTree as ET

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

# 使用示例
xml_folder_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/xml汇总'
integerize_coordinates(xml_folder_path)
