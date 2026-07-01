import os
import shutil
from collections import Counter

def find_duplicate_files(folders, output_folder):
    # 遍历所有文件夹，获取文件名列表
    all_files = []
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            all_files.extend(files)

    # 统计文件名出现的次数
    file_counts = Counter(all_files)

    # 找到重复的文件名
    duplicate_files = [file for file, count in file_counts.items() if count > 1]

    # 复制重复的文件到指定文件夹
    for duplicate_file in duplicate_files:
        for folder in folders:
            for root, dirs, files in os.walk(folder):
                if duplicate_file in files:
                    src_file = os.path.join(root, duplicate_file)
                    dst_file = os.path.join(output_folder, duplicate_file)
                    # 如果文件已经存在，则在文件名后加上'_copy'
                    if os.path.exists(dst_file):
                        base, ext = os.path.splitext(dst_file)
                        dst_file = f"{base}_copy{ext}"
                    shutil.copy2(src_file, dst_file)

    # 统计总样本量、重复样本数量和去重后的样本数量
    total_samples = len(all_files)
    duplicate_samples = len(duplicate_files)
    unique_samples = total_samples - duplicate_samples

    return total_samples, duplicate_samples, unique_samples

# 要扫描的文件夹路径
folders = ["/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/2016年各站点原始图片已整理",
            "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/2017年各站点原始图片已整理", 
            "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/2022年设备虫情图片and绿色防控平台图片",
            "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/outputs_cebaodengall", 
            "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/outputs_cebaodengall2",
              "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/高空测报灯2023",
              "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC标注文件/罗浩伦小虫数据集"]
# 指定文件夹，用于存放重复文件的副本
output_folder = "/home/yaoteam/yaoteam/yyc/mmdet_dino/重复的样本"

# 执行函数
total_samples, duplicate_samples, unique_samples = find_duplicate_files(folders, output_folder)

# 打印统计结果
print("总样本量:", total_samples)
print("重复样本数量:", duplicate_samples)
print("去重后的样本数量:", unique_samples)
