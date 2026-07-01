import os
import shutil

def copy_images(root_dir, destination_dir):
    # 遍历根目录下的所有文件和子目录
    for root, dirs, files in os.walk(root_dir):
        # 遍历当前目录下的文件
        for file in files:
            # 检查文件是否为图片文件
            if file.endswith(('.png', '.jpg', '.jpeg','.xml')):
                # 构建源文件路径和目标文件路径
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)
                
                # 复制文件
                shutil.copy2(source_path, destination_path)

# 根文件目录
# root_directory = r'/home/yaoteam/yaoteam/yyc/all_small_pic/all_small_pic' # 176080
# root_directory = r'/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_20240523多种类虫标记数据集_putong' # 180565
root_directory = r'/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/other1' # 241226
# root_directory = r'/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件' # 259859

# 目标目录
destination_directory = r'/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/other'

# 复制图片文件
copy_images(root_directory, destination_directory)

print("Images copied successfully!")

