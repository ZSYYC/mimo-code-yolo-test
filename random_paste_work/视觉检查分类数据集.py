# 任务：视觉检查分类数据集。具体要从图片分类数据集中，每个类别随机复制出一张图片保存至指定目录，图片名为类别标签。

import os
import random
import shutil

def copy_random_image(source_dir, dest_dir):
    # 获取所有类别的子目录
    categories = os.listdir(source_dir)

    for category in categories:
        category_path = os.path.join(source_dir, category)
        
        if os.path.isdir(category_path):
            # 获取该类别下的所有图片
            images = os.listdir(category_path)
            if images:
                # 随机选择一张图片
                random_image = random.choice(images)
                src_image_path = os.path.join(category_path, random_image)

                # 构造目标图片的路径
                dest_image_path = os.path.join(dest_dir, f"{category}.jpg")
                
                # 复制图片
                shutil.copy(src_image_path, dest_image_path)
                print(f"Copied {src_image_path} to {dest_image_path}")

source_directory = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train0806'
destination_directory = '/home/yaoteam/yaoteam/yyc/random_paste_work/视觉可视化图片1'

os.makedirs(destination_directory, exist_ok=True)
copy_random_image(source_directory, destination_directory)
