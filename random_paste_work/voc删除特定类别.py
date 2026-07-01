import os
import xml.etree.ElementTree as ET

def remove_annotation_by_class(xml_folder, class_name):
    # 遍历文件夹中的XML文件
    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml'):
            xml_path = os.path.join(xml_folder, filename)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # 遍历XML中的object标签
            for obj in root.findall('object'):
                # 找到类别名称标签
                name = obj.find('name').text
                # 如果类别名称为指定的类别，就删除这个object标签
                if name in class_name:
                    root.remove(obj)
            
            # 保存修改后的XML文件
            tree.write(xml_path)

# 示例用法
xml_folder1 = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/xml'
xml_folder2 = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/xml汇总20250225'
# class_name = 'Cotton leaf worm斜纹夜蛾类'  # 要删除的类别名字
class_to_remove = ['multitargets', 'olegs', 'insect', 'trash']
remove_annotation_by_class(xml_folder1, class_to_remove)
remove_annotation_by_class(xml_folder2, class_to_remove)

