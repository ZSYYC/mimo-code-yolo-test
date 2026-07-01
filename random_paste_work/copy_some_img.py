import os
import random
import shutil

def split_img_data(input_dir, output_dir, split_ratio):
            # 获取该类别下的所有文件
            files = os.listdir(input_dir)
            # 筛选出以'.jpg'结尾的文件
            jpg_files = [file for file in files if file.endswith('.jpg')]
            random.shuffle(jpg_files)  # 随机打乱文件顺序
            # 计算分割点
            split_point = int(len(jpg_files) * split_ratio)
            # 将一部分文件复制到新的目录
            for file in jpg_files[:split_point]:
                src_path = os.path.join(input_dir, file)
                dst_path = os.path.join(output_dir)
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)
                shutil.copy(src_path, dst_path) # 移动！！！！！！！！！！
# 示例用法

input_dir = "/home/yaoteam/yaoteam/yyc/mmdet_dino/佳多和云飞测报灯图片-津南/img"
output_dir = "/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img_0927/佳多和云飞测报灯图片_津南"
split_ratio = 0.2  # 指定的数据分割比例
split_img_data(input_dir, output_dir, split_ratio)
