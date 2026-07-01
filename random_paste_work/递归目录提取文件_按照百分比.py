import os
import shutil
import random

def copy_images(root_dir, destination_dir, percentage):
    total_images = 0
    total_copied = 0

    # 创建目标目录如果它不存在
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 遍历根目录下的所有文件和子目录
    for root, dirs, files in os.walk(root_dir):
        # 筛选出图片文件和XML文件
        image_files = [file for file in files if file.endswith(('.jpg', '.jpeg'))]

        # 随机抽取指定百分比的图片文件
        num_to_copy = int(len(image_files) * percentage / 100)
        selected_files = random.sample(image_files, num_to_copy)

        # 更新总计数
        total_images += len(image_files)
        total_copied += num_to_copy

        # 复制文件
        for file in selected_files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.copy2(source_path, destination_path)

        # 打印结果
        if image_files:
            print(f"Directory: {root}")
            print(f"Total images: {len(image_files)}")
            print(f"Images copied: {num_to_copy}")
            print("")

    print(f"Total images in all directories: {total_images}")
    print(f"Total images copied: {total_copied}")

# 根目录
root_directory = '/home/yaoteam/yaoteam/yyc/all_unlabeled_img0730_0_1/insect'
# 目标目录
destination_directory = '/home/yaoteam/yaoteam/yyc/random_paste_work/smallest_dataset_for_Mac'
# 提取百分比
percentage_to_copy = 1  # 修改此值以设置所需的百分比

# 复制图片文件
copy_images(root_directory, destination_directory, percentage_to_copy)
print("Images copied successfully!")
