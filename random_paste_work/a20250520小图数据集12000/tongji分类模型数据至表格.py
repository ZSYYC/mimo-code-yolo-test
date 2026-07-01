import os
import pandas as pd

def count_files_in_folders(input_folder):
    # 初始化计数器
    folder_file_count = {}
    total_files = 0
    total_folders = 0

    # 遍历 input_folder 中的每个子文件夹
    for sub_folder in os.listdir(input_folder):
        sub_folder_path = os.path.join(input_folder, sub_folder)
        
        if os.path.isdir(sub_folder_path):
            total_folders += 1
            file_count = len([f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))])
            folder_file_count[sub_folder] = file_count
            total_files += file_count

    return folder_file_count, total_folders, total_files

# 指定 input_folder 路径
input_folder = '/home/star/2T/yyc/2024summer_biaozhu_small_img/2024summer_biaozhu_small_img_12000'

# 统计文件数量
folder_file_count, total_folders, total_files = count_files_in_folders(input_folder)

# 将结果转换为 DataFrame 并按数量降序排序
df = pd.DataFrame(list(folder_file_count.items()), columns=['insect Name', 'insect Count'])
df = df.sort_values(by='insect Count', ascending=False)

# 输出 Excel 文件
output_path = '/home/star/2T/yyc/2024summer_biaozhu_small_img/folder_file_counts.xlsx'
df.to_excel(output_path, index=False)

# 输出统计信息
print(f"Total number of folders: {total_folders}")
print(f"Total number of files: {total_files}")
print(f"Statistics saved to {output_path}")
