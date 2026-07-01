import os
import xml.etree.ElementTree as ET

def check_name_contains_char(xml_folder, target_char):
    matched_files = []

    for filename in os.listdir(xml_folder):
        if not filename.endswith(".xml"):
            continue

        xml_path = os.path.join(xml_folder, filename)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for obj in root.findall("object"):
            name = obj.find("name").text.strip()
            if target_char in name:
                matched_files.append((filename, name))
                break  # 一个文件中有一个匹配就记录

    print(f"找到包含字符 '{target_char}' 的文件共 {len(matched_files)} 个：")
    for file, label in matched_files:
        print(f"文件: {file}, 标签: {label}")

# 用法示例
xml_dir = "/home/yaoteam/yaoteam/wz/voc2coco/VOC/Annotations/"  # 替换为你的 XML 文件夹路径
target_character = "小虫16-烁划蝽属"
check_name_contains_char(xml_dir, target_character)