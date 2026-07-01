import os
import shutil
from tqdm import tqdm

def split_img_data(input_dir, output_dir, interval):
    # 获取该类别下的所有文件
    files = os.listdir(input_dir)
    # 筛选出以'.jpg'结尾的文件
    jpg_files = [file for file in files if file.endswith('.jpg')]
    # 按照文件名排序
    jpg_files.sort()
    # 按照间隔进行采样
    sampled_files = jpg_files[::interval]
    # 将采样的文件复制到新的目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file in tqdm(sampled_files, desc="Copying files", unit="file"):
        src_path = os.path.join(input_dir, file)
        dst_path = os.path.join(output_dir, file)
        shutil.copy(src_path, dst_path)

# 示例用法
input_dir = "/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images"
output_dir = "/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img_0927/数据集抽样100"
interval = 100  # 指定的间隔数
split_img_data(input_dir, output_dir, interval)
