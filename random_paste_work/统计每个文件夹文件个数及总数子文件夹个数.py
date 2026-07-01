import os

import pandas as pd

# 读取CSV文件
csv_file = '/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi.csv'
df = pd.read_csv(csv_file)

# 创建标签映射字典
label_mapping = dict(zip(df['ret'], df['name']))


def count_files_in_folders(input_folder):
    # 初始化计数器
    folder_file_count = {}
    total_files = 0
    total_folders = 0

    # 遍历input_folder中的每个子文件夹
    for sub_folder in os.listdir(input_folder):
        sub_folder_path = os.path.join(input_folder, sub_folder)
        
        if os.path.isdir(sub_folder_path):
            total_folders += 1
            file_count = len([f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))])
            folder_file_count[sub_folder] = file_count
            total_files += file_count

    return folder_file_count, total_folders, total_files

# 指定input_folder路径
input_folder = '/home/star/2T/yyc/2024summer_biaozhu_small_img_20250522/2024summer_biaozhu_small_img_12000_train3000/train'
# input_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train3000/train/'

# 统计文件数量
folder_file_count, total_folders, total_files = count_files_in_folders(input_folder)

# 输出结果
print(f"Total number of folders: {total_folders}")
print(f"Total number of files: {total_files}")
print("Number of files in each folder:")
for folder, count in folder_file_count.items():
    print(f"{label_mapping.get(folder, folder)}: {count} files")
