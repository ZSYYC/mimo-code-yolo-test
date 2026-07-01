import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def bytes_to_gb(size_in_bytes):
    gb_size = size_in_bytes / (1024 ** 3)
    return gb_size

def calculate_folder_sizes(folder_paths):
    folder_sizes = {}
    total_size = 0
    for folder_path in folder_paths:
        size = get_folder_size(folder_path)
        folder_sizes[folder_path] = size
        total_size += size
    return folder_sizes, total_size

# 要计算内存大小的文件夹路径列表
folders = ["/home/yaoteam/yaoteam/yyc/YYC_SSD/cebaodengall/JPEGImages", 
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/cebaodengall/JPEGImages2", 
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/2022年设备虫情图片and绿色防控平台图片",
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/2017年各站点原始图片已整理", 
           "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/2016年各站点原始图片已整理", 
           "/home/yaoteam/yaoteam/yyc/random_paste_work/虫情测报灯罗浩伦数据集/VOC/JPEGImages",]

# 计算各文件夹的大小和总共的大小
folder_sizes, total_size = calculate_folder_sizes(folders)

# 转换为 GB
total_size_gb = bytes_to_gb(total_size)
folder_sizes_gb = {folder_path: bytes_to_gb(size) for folder_path, size in folder_sizes.items()}

# 打印各文件夹的大小和总共的大小
for folder_path, size in folder_sizes_gb.items():
    print(f"文件夹 {folder_path} 的大小为: {size} GB")
print(f"所有文件夹总共的大小为: {total_size_gb} GB")
