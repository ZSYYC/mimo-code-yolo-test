import os
import hashlib

def calculate_md5(file_path):
    """Calculate MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_directories(dir1, dir2):
    """Compare two directories for files with the same name and content."""
    dir1_files = {file for file in os.listdir(dir1) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))}
    dir2_files = {file for file in os.listdir(dir2) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))}
    
    common_files = dir1_files & dir2_files  # Intersection of both sets
    identical_files_count = 0
    
    for file in common_files:
        file1_path = os.path.join(dir1, file)
        file2_path = os.path.join(dir2, file)
        
        if calculate_md5(file1_path) == calculate_md5(file2_path):
            identical_files_count += 1
    
    return identical_files_count

# 目录路径
directory1 = '/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总'
directory2 = '/home/yaoteam/yaoteam/yyc/random_paste_work/cebaodeng_good_picture'

# 比较目录并打印结果
identical_files_count = compare_directories(directory1, directory2)
print(f"Number of identical files: {identical_files_count}")
