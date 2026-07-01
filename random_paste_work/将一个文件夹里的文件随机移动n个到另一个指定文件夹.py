import os
import random
import shutil

def move_random_images(src_folder, dst_folder, num_images):
    # 获取源文件夹中的所有图片
    images = os.listdir(src_folder)

    # 检查是否有足够的图片可以移动
    if len(images) < num_images:
        print(f"Not enough images in {src_folder} to move {num_images} images.")
        return

    # 随机选择 num_images 张图片
    selected_images = random.sample(images, num_images)

    # 确保目标文件夹存在
    os.makedirs(dst_folder, exist_ok=True)

    # 移动选中的图片到目标文件夹
    for image in selected_images:
        src_path = os.path.join(src_folder, image)
        dst_path = os.path.join(dst_folder, image)
        shutil.move(src_path, dst_path)
        print(f"Moved {src_path} to {dst_path}")

# 示例用法
src_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/虫情测报灯图片/part1'
dst_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/虫情测报灯图片/part3'
num_images = 400

move_random_images(src_folder, dst_folder, num_images)
