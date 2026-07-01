import os
from PIL import Image


# 判断文件是否是图片
def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()  # 验证是否为有效的图片
        return True
    except (IOError, SyntaxError):
        return False


# 统计文件夹中每个子文件夹中的图片数量，并输出所有图片的总数
def count_images_in_subfolders(folder_path):
    total_images = 0  # 记录所有图片的总数量
    # 遍历指定文件夹
    for root, dirs, files in os.walk(folder_path):
        # 排除根文件夹，只处理子文件夹
        if root == folder_path:
            continue

        image_count = 0
        # 遍历每个文件
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file_path):  # 如果是图片文件
                image_count += 1

        print(f"子文件夹: {root}, 图片数量: {image_count}")
        total_images += image_count  # 累计图片总数

    print(f"\n所有图片的总数: {total_images}")


# 设置要检查的文件夹路径
folder_path = "/home/star/8T/wz/voc2coco/两种标签裁剪小图"
count_images_in_subfolders(folder_path)