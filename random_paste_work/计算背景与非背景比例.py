import os
import xml.etree.ElementTree as ET

# 设置 XML 文件所在目录
xml_dir = '/home/yaoteam/yaoteam/wz/voc2coco/VOC/Annotations/'  # <-- 修改为你实际的路径

background_count = 0
non_background_count = 0
total_files = 0

for filename in os.listdir(xml_dir):
    if filename.endswith('.xml'):
        total_files += 1
        file_path = os.path.join(xml_dir, filename)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            objects = root.findall('object')
            if len(objects) == 0:
                background_count += 1
            else:
                non_background_count += 1
        except Exception as e:
            print(f"解析出错：{filename}，错误信息：{e}")

# 输出统计结果
print(f'总文件数: {total_files}')
print(f'背景文件数（无object）: {background_count}')
print(f'含标注文件数: {non_background_count}')
if total_files > 0:
    print(f'背景比例: {background_count / total_files:.2%}')
    print(f'标注比例: {non_background_count / total_files:.2%}')