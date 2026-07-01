import os
import random
import shutil
from PIL import Image, ImageEnhance, ImageOps

def image_augmentation(img_path):
    img = Image.open(img_path).convert("RGB")

    # 进行随机变换
    if random.random() > 0.5:
        img = ImageOps.mirror(img)
    if random.random() > 0.5:
        img = ImageOps.flip(img)
    if random.random() > 0.5:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))
    if random.random() > 0.5:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(random.uniform(0.7, 1.3))

    return img

def balance_dataset(input_folder, output_folder, threshold_n):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for sub_folder in os.listdir(input_folder):
        sub_folder_path = os.path.join(input_folder, sub_folder)

        if not os.path.isdir(sub_folder_path):
            continue

        file_list = [f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))]
        file_count = len(file_list)

        if file_count < threshold_n:
            print(f'{sub_folder} 类别的数量太少，跳过')
            continue

        target_folder = os.path.join(output_folder, sub_folder)
        os.makedirs(target_folder, exist_ok=True)

        if file_count < 50:
            # 复制原始文件
            for file in file_list:
                shutil.copy(os.path.join(sub_folder_path, file), target_folder)

            # 增强数据到 50 张
            while file_count < 50:
                file_to_augment = random.choice(file_list)
                img = image_augmentation(os.path.join(sub_folder_path, file_to_augment))
                new_file_name = f"{os.path.splitext(file_to_augment)[0]}_augment_{file_count}.jpg"
                img.save(os.path.join(target_folder, new_file_name), quality=100)
                file_count += 1
        elif file_count > 5000:
            sampled_files = random.sample(file_list, 5000)
            for file in sampled_files:
                shutil.copy(os.path.join(sub_folder_path, file), target_folder)
        else:
            for file in file_list:
                shutil.copy(os.path.join(sub_folder_path, file), target_folder)

    print("Dataset balancing completed.")

# 设置参数
input_folder = "/home/star/2T/yyc/2024summer_biaozhu_small_img/2024summer_biaozhu_small_img_12000"
output_folder = "/home/star/2T/yyc/2024summer_biaozhu_small_img/dataset/train"
threshold_n = 0  # 可调阈值 选择小于该阈值的抛弃

# 运行脚本
balance_dataset(input_folder, output_folder, threshold_n)
