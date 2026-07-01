import os
import shutil
import random

def split_dataset(source_dir, train_dir, val_dir, train_ratio=0.8):
    # 确保训练集和验证集目录存在
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    # 获取所有类别的子文件夹
    categories = [folder for folder in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, folder))]
    
    # 对每个类别进行处理
    for category in categories:
        category_path = os.path.join(source_dir, category)
        
        # 获取该类别下的所有图片文件
        images = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
        
        # 随机打乱图片列表
        random.shuffle(images)
        
        # 根据给定的比例分割数据集
        split_index = int(len(images) * train_ratio)
        train_images = images[:split_index]
        val_images = images[split_index:]
        
        # 创建该类别下的训练集和验证集文件夹
        os.makedirs(os.path.join(train_dir, category), exist_ok=True)
        os.makedirs(os.path.join(val_dir, category), exist_ok=True)
        
        # 将图片复制到训练集和验证集文件夹中
        for img in train_images:
            shutil.copy(os.path.join(category_path, img), os.path.join(train_dir, category, img))
        
        for img in val_images:
            shutil.copy(os.path.join(category_path, img), os.path.join(val_dir, category, img))
        
        print(f"类别 {category} 已分割 {len(train_images)} 张图片到训练集，{len(val_images)} 张图片到验证集。")

# 设置源文件夹路径、训练集和验证集目标文件夹路径
source_folder = '/home/yaoteam/yaoteam/wz/飞虱叶蝉原始训练数据集_种/'  # 数据集文件夹路径
train_folder = '/home/yaoteam/yaoteam/wz/飞虱叶蝉训练集_种/train/'    # 训练集目标文件夹路径
val_folder = '/home/yaoteam/yaoteam/wz/飞虱叶蝉训练集_种/val/'        # 验证集目标文件夹路径

# 调用函数进行数据集划分
split_dataset(source_folder, train_folder, val_folder, train_ratio=0.8)