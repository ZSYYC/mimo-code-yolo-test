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

# 图片文件夹路径
image_dir = '/home/yaoteam/yaoteam/wz/oss图片及其对应xml/images/'
# 输出 XML 文件夹
output_dir = '/home/yaoteam/yaoteam/wz/oss图片及其对应xml/xml'
os.makedirs(output_dir, exist_ok=True)

# 标签白名单（只保留这些标签）
# allowed_tags = {"L1", "L2", "B4", "B5", "L9"}

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

# 遍历图片文件夹
for filename in os.listdir(image_dir):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    image_path = os.path.join(image_dir, filename)

    # 获取图像尺寸
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            depth = len(img.getbands())
    except Exception as e:
        print(f"[错误] 无法读取图像尺寸：{filename}, 错误：{e}")
        continue

    # 查询数据库
    sql = "SELECT tag_for_draw, corner FROM ser_traplight_photo WHERE photo_path LIKE %s"
    cursor.execute(sql, ('%' + filename,))
    result = cursor.fetchone()

    if result is None:
        print(f"[跳过] 数据库中未找到：{filename}")
        continue

    tag_raw, corner_raw = result

    try:
        if not tag_raw or tag_raw.strip() == '' or not corner_raw or corner_raw.strip() == '':
            print(f"[跳过] {filename} 的 tag 或 corner 字段为空")
            continue

        tag_dict = json.loads(tag_raw)
        corner_list = json.loads(corner_raw)

        if not isinstance(tag_dict, list) or not isinstance(corner_list, list):
            print(f"[跳过] {filename} tag/corner 类型错误")
            continue

    except json.JSONDecodeError as e:
        print(f"[JSON错误] {filename}：{e}")
        continue

    # 展平标签
    # labels_expanded = []
    # for label, count in tag_dict.items():
    #     labels_expanded.extend([label] * count)

    if len(tag_dict) != len(corner_list):
        print(f"[跳过] 标签数量 ({len(tag_dict)}) 与 corner 数量 ({len(corner_list)}) 不匹配：{filename}")
        continue

    objects = []
    for label, coords in zip(tag_dict, corner_list):
        # if label not in allowed_tags:
        #     continue

        xmin, ymin, xmax, ymax = coords
        objects.append({
            'name': label,
            'xmin': int(xmin),
            'ymin': int(ymin),
            'xmax': int(xmax),
            'ymax': int(ymax)
        })

    if not objects:
        print(f"[跳过] {filename} 中没有符合条件的标签")
        continue
    # 写入 XML 文件
    xml_tree = create_pascal_voc_xml(filename, width, height, depth, objects)
    xml_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.xml')
    xml_tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    print(f"[完成] 生成标注文件：{xml_path}")

cursor.close()
connection.close()