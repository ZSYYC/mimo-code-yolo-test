import os
import pymysql
import xml.etree.ElementTree as ET
from PIL import Image
import json

# MySQL 连接信息
db_config = {
    'host': '121.199.54.94',
    'user': 'root',
    'password': 'ZsTu@Ecs@2025',
    'database': 'ry-vue-zdnzw',
    'charset': 'utf8mb4'
}

# 筛选条件
target_device_name = 'CwuGZnD6R2rLdnnWP4se'
start_time = '2024-09-01 00:00:00'
end_time = '2024-12-31 24:00:00'
# 输出 XML 文件夹
output_dir = '/home/yaoteam/yaoteam/wz/oss图片对应xml/'
os.makedirs(output_dir, exist_ok=True)


# 连接数据库
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

def create_pascal_voc_xml(filename, width, height, depth, objects):
    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'filename').text = filename

    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)

    for obj in objects:
        object_tag = ET.SubElement(annotation, 'object')
        ET.SubElement(object_tag, 'name').text = obj['name']
        bndbox = ET.SubElement(object_tag, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(obj['xmin'])
        ET.SubElement(bndbox, 'ymin').text = str(obj['ymin'])
        ET.SubElement(bndbox, 'xmax').text = str(obj['xmax'])
        ET.SubElement(bndbox, 'ymax').text = str(obj['ymax'])

    return ET.ElementTree(annotation)

# 查询满足条件的图片信息（包括 photo_name 和 photo_path）
sql = """
    SELECT photo_name, photo_path, tag_for_draw, corner
    FROM ser_traplight_photo
    WHERE device_name = %s AND photo_time BETWEEN %s AND %s
"""
cursor.execute(sql, (target_device_name, start_time, end_time))
results = cursor.fetchall()

# 结果格式：[(photo_name, photo_path, tag, corner), ...]

for photo_name, photo_path, tag_raw, corner_raw in results:
    image_path = os.path.join(image_dir, photo_name)
    if not os.path.exists(image_path):
        print(f"[跳过] 图像文件不存在：{image_path}")
        continue

    # 获取图像尺寸
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            depth = len(img.getbands())
    except Exception as e:
        print(f"[错误] 无法读取图像尺寸：{photo_name}, 错误：{e}")
        continue

    # 检查并解析标签与坐标
    try:
        if not tag_raw or not corner_raw:
            print(f"[跳过] {photo_name} 的 tag 或 corner 字段为空")
            continue

        tag_dict = json.loads(tag_raw)
        corner_list = json.loads(corner_raw)

        if not isinstance(tag_dict, dict) or not isinstance(corner_list, list):
            print(f"[跳过] {photo_name} tag/corner 类型错误")
            continue
    except json.JSONDecodeError as e:
        print(f"[JSON错误] {photo_name}：{e}")
        continue

    # labels_expanded = []
    # for label, count in tag_dict.items():
    #     labels_expanded.extend([label] * count)
    #
    if len(tag_dict) != len(corner_list):
        print(f"[跳过] 标签数量 ({len(tag_dict)}) 与 corner 数量 ({len(corner_list)}) 不匹配：{photo_name}")
        continue

    objects = []
    for label, coords in zip(tag_dict, corner_list):
        xmin, ymin, xmax, ymax = coords
        objects.append({
            'name': label,
            'xmin': int(xmin),
            'ymin': int(ymin),
            'xmax': int(xmax),
            'ymax': int(ymax)
        })

    # 写入 XML
    xml_tree = create_pascal_voc_xml(photo_name, width, height, depth, objects)
    xml_path = os.path.join(output_dir, os.path.splitext(photo_name)[0] + '.xml')
    xml_tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    print(f"[完成] 生成标注文件：{xml_path}")

cursor.close()
connection.close()