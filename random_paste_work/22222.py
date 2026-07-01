import os
import xml.etree.ElementTree as ET
import re
from shutil import copyfile

def is_chinese(text):
    """判断字符串是否全为中文"""
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)

def filter_xml_keep_chinese_objects(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.endswith(".xml"):
            continue

        tree = ET.parse(os.path.join(input_dir, filename))
        root = tree.getroot()
        objects = root.findall("object")

        removed_count = 0
        for obj in objects:
            name = obj.find("name").text
            if not is_chinese(name):
                root.remove(obj)
                removed_count += 1

        # 即使没有目标也保存文件
        output_path = os.path.join(output_dir, filename)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

        print(f"✔️ 处理完成：{filename}，移除 {removed_count} 个非中文目标")

# 示例用法
filter_xml_keep_chinese_objects("/home/yaoteam/yaoteam/wz/oss图片及其对应xml/annotations/", "/home/yaoteam/yaoteam/wz/oss图片及其对应xml/new_annotations/")