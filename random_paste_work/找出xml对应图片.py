import os
import shutil
import xml.etree.ElementTree as ET

# 配置路径
xml_dir = '/home/yaoteam/yaoteam/wz/oss图片对应xml/'               # XML 文件夹
image_dir = '/home/yaoteam/yaoteam/wz/oss图片下载/兴化周庄镇/'           # 所有图片所在目录
output_image_dir = '/home/yaoteam/yaoteam/wz/oss图片及其对应xml/images/'   # 复制目标目录
os.makedirs(output_image_dir, exist_ok=True)

# 支持的图片后缀
image_exts = ['.jpg', '.jpeg', '.png']

# 遍历所有 XML 文件
for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith('.xml'):
        continue

    xml_path = os.path.join(xml_dir, xml_file)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        filename = root.find('filename').text

        # 在原始图片目录中查找该文件
        image_path = os.path.join(image_dir, filename)
        if os.path.exists(image_path):
            shutil.copy(image_path, os.path.join(output_image_dir, filename))
            print(f"[✓] 复制成功: {filename}")
        else:
            print(f"[✗] 找不到图片: {filename}")

    except Exception as e:
        print(f"[错误] 处理 {xml_file} 时出错: {e}")