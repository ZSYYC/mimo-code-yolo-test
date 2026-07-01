import os
import shutil

def copy_matching_xml(image_folder, xml_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 获取图片文件夹中的所有文件名（不包括扩展名）
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # 遍历图片文件
    for image_file in image_files:
        # 获取文件名（去除扩展名）
        image_name, _ = os.path.splitext(image_file)

        # 查找对应的 XML 文件
        xml_file = image_name + '.xml'
        xml_file_path = os.path.join(xml_folder, xml_file)

        # 如果找到对应的 XML 文件，则复制到目标文件夹
        if os.path.exists(xml_file_path):
            shutil.copy(xml_file_path, os.path.join(output_folder, xml_file))
            print(f"已复制 {xml_file} 到 {output_folder}")

# 设置文件夹路径
image_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/0529_dataset_dataugmentation/image10/'  # 替换为图片文件夹路径
xml_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/0529_dataset_dataugmentation/xml/'      # 替换为XML文件夹路径
output_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/0529_dataset_dataugmentation/xml10/'  # 替换为新文件夹路径

# 调用函数进行复制
copy_matching_xml(image_folder, xml_folder, output_folder)