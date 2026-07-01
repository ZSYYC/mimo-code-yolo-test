import os
import shutil
from tqdm import tqdm

def merge_folders(input_folders, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    total_files = 0
    # First, count the total number of files to copy
    for input_folder in input_folders:
        for sub_folder in os.listdir(input_folder):
            src_sub_folder_path = os.path.join(input_folder, sub_folder)
            if os.path.isdir(src_sub_folder_path):  # Check if it is a directory
                total_files += len(os.listdir(src_sub_folder_path))

    with tqdm(total=total_files, desc="Merging folders") as pbar:
        for input_folder in input_folders:
            for sub_folder in os.listdir(input_folder):
                src_sub_folder_path = os.path.join(input_folder, sub_folder)
                if os.path.isdir(src_sub_folder_path):  # Check if it is a directory
                    dest_sub_folder_path = os.path.join(output_folder, sub_folder)

                    if not os.path.exists(dest_sub_folder_path):
                        os.makedirs(dest_sub_folder_path)

                    for file_name in os.listdir(src_sub_folder_path):
                        src_file_path = os.path.join(src_sub_folder_path, file_name)
                        dest_file_path = os.path.join(dest_sub_folder_path, file_name)

                        if not os.path.exists(dest_file_path):
                            shutil.copy(src_file_path, dest_file_path)
                        else:
                            # Skip the file if it already exists
                            print(f"File {dest_file_path} already exists. Skipping.")
                        
                        pbar.update(1)

# 小图所有已分类数据集：1. 水稻所最新拍摄的单种虫数据集截止0606 2. 罗浩伦大小虫数据集 3. 尤彦辰拍摄的9种虫数据集
input_folders = ['/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_20240523多种类虫标记数据集_putong_训练集', '/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_cebaodengall_putong', '/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_cebaodengall2_putong','/home/yaoteam/yaoteam/yyc/Swin-Transformer/data/crop_putong_9/train','/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_bbfshfsyechan_lhl_putong']
output_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/小图训练集所有已分类图片'

merge_folders(input_folders, output_folder)
