import os
import xml.etree.ElementTree as ET
import shutil

def process_xml_files(input_folder, output_folder, categories_to_process, keep_categories=True):
    """
    处理VOC格式的XML文件，删除或保留指定类别的标注。

    :param input_folder: 输入的XML标注文件夹路径
    :param output_folder: 输出的XML文件夹路径
    :param categories_to_process: 需要删除或者保留的类别列表
    :param keep_categories: 如果为True，保留指定类别；否则删除指定类别
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有xml文件
    xml_files = [f for f in os.listdir(input_folder) if f.endswith('.xml')]

    for xml_file in xml_files:
        file_path = os.path.join(input_folder, xml_file)
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 获取所有的object节点
        objects = root.findall('object')

        # 处理每个object节点
        for obj in objects:
            category = obj.find('name').text
            if keep_categories:
                if category not in categories_to_process:
                    root.remove(obj)  # 如果不在保留类别中，删除该object
            else:
                if category in categories_to_process:
                    root.remove(obj)  # 如果在删除类别中，删除该object

        # 将处理后的XML文件保存到输出文件夹
        output_file_path = os.path.join(output_folder, xml_file)
        tree.write(output_file_path)

    print(f"处理完成！修改后的XML文件已保存至: {output_folder}")

# 示例用法
input_folder = "/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/xml"  # 输入的xml文件夹路径
output_folder = "/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/few_xml"  # 输出的xml文件夹路径
categories_to_process = ["B4", "B12","L47", "L1","L2", "L41","Q7"]  # 要删除或保留的类别
keep_categories = True  # 设置为True表示保留指定类别，False表示删除指定类别

process_xml_files(input_folder, output_folder, categories_to_process, keep_categories)
