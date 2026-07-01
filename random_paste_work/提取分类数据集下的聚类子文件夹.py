# Python实现，给定一个root文件夹路径，里面包含有图片文件、子文件夹，子文件夹里又包含图片文件或者文件夹，以此类推，现在要将子文件夹里的图片全部都提取到给定的root文件夹中且删除所有子文件夹，以下是示例：
# root folder
# 	--sub folder1
# 		--img1
# 		--img2
# 	--sub folder2
# 		--sub sub folder3
# 			--img6
# 		--img3
# 	--img4
# 	--img5
# 处理完后应变为
# root folder
# 	--img1
# 	--img2
# 	--img3
# 	--img4
# 	--img5
# 	--img6

import os
import shutil

def extract_and_flatten_images(root_folder):
    # 遍历 root 文件夹及其子文件夹
    for root, dirs, files in os.walk(root_folder, topdown=False):
        for file in files:
            # 构建文件的完整路径
            file_path = os.path.join(root, file)
            # 构建目标路径
            destination_path = os.path.join(root_folder, file)

            # 检查目标路径是否存在同名文件
            if os.path.exists(destination_path):
                # print(f"Skipping {file} as it already exists in {root_folder}")
                continue  # 跳过这个文件

            # 移动文件到 root 文件夹
            shutil.move(file_path, destination_path)
            print(f'文件被移动至root目录: {file_path}')

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)  # 尝试删除子文件夹
            except OSError:
                print(f"Force deleting {dir_path} as it is not empty.")
                shutil.rmtree(dir_path)  # 强制删除文件夹及其内容

def process_multiple_roots(parent_folder):
    # 遍历上一级目录下的所有文件夹
    for item in os.listdir(parent_folder):
        root_folder = os.path.join(parent_folder, item)
        if os.path.isdir(root_folder):
            print(f"Processing folder: {root_folder}")
            extract_and_flatten_images(root_folder)
# 使用示例
train_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/招标用数据集20240830/train0806'
process_multiple_roots(train_folder)