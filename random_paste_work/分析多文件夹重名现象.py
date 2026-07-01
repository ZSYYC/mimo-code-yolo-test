import os
from collections import defaultdict

def get_file_counts(directories):
    total_files = defaultdict(int)
    unique_files = defaultdict(set)
    jpg_files = defaultdict(int)
    all_files = defaultdict(set)
    
    # Collect file information
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                
                total_files[directory] += 1
                all_files[directory].add(file_name)
                
                if file.lower().endswith('.jpg'):
                    jpg_files[directory] += 1
    
    # Determine unique files
    for directory in directories:
        other_files = set()
        for other_dir in directories:
            if other_dir != directory:
                other_files.update(all_files[other_dir])
        
        unique_files[directory] = all_files[directory] - other_files

    return total_files, unique_files, jpg_files

def print_file_statistics(directories):
    total_files, unique_files, jpg_files = get_file_counts(directories)
    
    for directory in directories:
        print(f"Directory: {directory}")
        print(f"Total files: {total_files[directory]}")
        print(f"Unique files: {len(unique_files[directory])}")
        print(f"JPG files: {jpg_files[directory]}")
        print("")

# 指定要统计的文件夹
directories = [
    '/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总',
    '/home/yaoteam/yaoteam/yyc/random_paste_work/cebaodeng_good_picture',
    # '/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_mmdino_pseudo_0630',
    # 添加更多文件夹路径
]

# 打印统计信息
print_file_statistics(directories)
