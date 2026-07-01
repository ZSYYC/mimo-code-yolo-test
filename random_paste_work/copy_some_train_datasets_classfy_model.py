import os
import random
import shutil

def split_imagenet_data(input_dir, output_dir, split_ratio):
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # 遍历ImageNet训练集的子目录
        for class_name in os.listdir(input_dir):
            class_dir = os.path.join(input_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
            # 获取该类别下的所有文件
            files = os.listdir(class_dir)
            random.shuffle(files)  # 随机打乱文件顺序
            # 计算分割点
            split_point = int(len(files) * split_ratio)
            # split_point = 100 # 每个类别复制固定数量的图片
            # 将一部分文件复制到新的目录
            for file in files[:split_point]:
                src_path = os.path.join(class_dir, file)
                dst_path = os.path.join(output_dir, class_name)
                if not os.path.exists(dst_path):
                    os.makedirs(dst_path)
                shutil.copy(src_path, dst_path)
        print("Splitting completed.")
# 示例用法
# !!!!!!!!!!!!!!!需要填写根目录路径，单类别的要填上一个目录
input_dir = "/home/yaoteam/yaoteam/yyc/all_small_pic_labeled/all_small_pic_datasets/train"
output_dir = "/home/yaoteam/yaoteam/yyc/random_paste_work/tsne_可视化数据集_部分类别/class36"
split_ratio = 0.1  # 指定的数据分割比例
split_imagenet_data(input_dir, output_dir, split_ratio)
