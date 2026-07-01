import os
import xml.etree.ElementTree as ET

# 中文对照表（标签名映射）
name_map = {
    "B4": "小虫1-褐飞虱属",
    "B5": "小虫2-白背飞虱",
    "B6": "小虫4-灰飞虱",
    # 可继续添加...
}

# XML 文件夹路径
xml_dir = '/home/yaoteam/yaoteam/wz/oss图片及其对应xml/xml/'  # 替换为你的 XML 文件夹路径

# 遍历 XML 文件夹
for filename in os.listdir(xml_dir):
    if not filename.endswith('.xml'):
        continue

    xml_path = os.path.join(xml_dir, filename)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"[错误] 无法解析 XML 文件 {filename}：{e}")
        continue

    has_matched = False  # 是否存在匹配的标签
    total_objects = 0    # object 总数
    matched_objects = 0  # 被替换的标签数

    for obj in root.findall('object'):
        total_objects += 1
        name_elem = obj.find('name')
        if name_elem is not None:
            label = name_elem.text
            if label in name_map:
                name_elem.text = name_map[label]
                has_matched = True
                matched_objects += 1

    if has_matched:
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        print(f"[已更新] 替换完成：{filename}，共 {matched_objects}/{total_objects} 个标签被替换")
    else:
        os.remove(xml_path)
        print(f"[已删除] 未匹配任何标签：{filename}")