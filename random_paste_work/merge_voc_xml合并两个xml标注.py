import os
import shutil
import xml.etree.ElementTree as ET

def merge_voc_xml(xml_a, xml_b):
    # 解析第一个XML文件
    tree_a = ET.parse(xml_a)
    root_a = tree_a.getroot()

    # 解析第二个XML文件
    tree_b = ET.parse(xml_b)
    root_b = tree_b.getroot()

    # 获取第一个XML文件中的所有<object>标签
    objects_a = root_a.findall('object')

    # 获取第二个XML文件中的所有<object>标签
    objects_b = root_b.findall('object')

    # 合并<object>标签
    for obj in objects_b:
        root_a.append(obj)  # 将第二个XML文件的object标签添加到第一个XML文件

    # 返回合并后的树
    return tree_a

def merge_xml_files_in_dirs(dir_a, dir_b, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 获取两个目录中所有文件的名称
    files_a = os.listdir(dir_a)

    for file_name in files_a:
        if file_name.endswith('.xml'):
            # 获取XML文件的完整路径
            xml_a = os.path.join(dir_a, file_name)
            xml_b = os.path.join(dir_b, file_name)

            # 合并两个XML文件
            if os.path.exists(xml_b):
                merged_tree = merge_voc_xml(xml_a, xml_b)

                # 保存合并后的文件
                output_path = os.path.join(output_dir, file_name)
                merged_tree.write(output_path)
                print(f"已合并并保存文件: {output_path}")

# 示例用法
dir_a = '/home/yaoteam/yaoteam/yyc/random_paste_work/数据集/小虫/xml'  # 第一个文件夹路径
dir_b = '/home/yaoteam/yaoteam/yyc/random_paste_work/数据集/大虫/xml'  # 第二个文件夹路径  数据库
output_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/数据集/大小虫/xml'  # 合并后的输出目录路径
merge_xml_files_in_dirs(dir_a, dir_b, output_dir)