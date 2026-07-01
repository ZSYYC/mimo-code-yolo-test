import os
import shutil
from tqdm import tqdm

def copy_images_to_folder(src_dirs, dest_dir, image_extensions=['.jpg', '.jpeg', '.png', '.bmp']):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for src_dir in src_dirs:
        for root, _, files in os.walk(src_dir):
            for file in tqdm(files, desc=f"Copying from {src_dir}"):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    src_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(dest_dir, file)
                    shutil.copy2(src_file_path, dest_file_path)

# 设置源文件夹和目标文件夹
src_dirs = [
            "/home/yaoteam/yaoteam/yyc/YYC_SSD/cebaodengall/JPEGImages", 
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/cebaodengall/JPEGImages2", 
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/2022年设备虫情图片and绿色防控平台图片",
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/2017年各站点原始图片已整理", 
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/2016年各站点原始图片已整理", 
        #    "/home/yaoteam/yaoteam/yyc/random_paste_work/虫情测报灯罗浩伦数据集/VOC/JPEGImages"（软链接的方式）
        # ,"/home/yaoteam/yaoteam/yyc/YYC_SSD/2023年高空测报灯图像/cebaodeng_good_picture/"
]
dest_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总'

copy_images_to_folder(src_dirs, dest_dir)
