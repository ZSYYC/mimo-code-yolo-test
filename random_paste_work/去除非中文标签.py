import os
import xml.etree.ElementTree as ET
import re

def is_chinese(text):
    """判断字符串中是否包含至少一个中文字符"""
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)

def remove_non_chinese_labels(xml_folder):
    for filename in os.listdir(xml_folder):
        if not filename.endswith('.xml'):
            continue

        path = os.path.join(xml_folder, filename)
        tree = ET.parse(path)
        root = tree.getroot()

        objects = root.findall('object')
        removed = False

        for obj in objects:
            name = obj.find('name').text.strip()
            if not is_chinese(name):
                root.remove(obj)
                removed = True
                print(f"[已移除] 文件 {filename} 中标签 '{name}' 为非中文")

        if removed:
            tree.write(path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    xml_folder = '/home/yaoteam/yaoteam/wz/13019图片_整合oss_去除小虫标注/xml'  # 替换为你的 XML 文件夹路径
    remove_non_chinese_labels(xml_folder)