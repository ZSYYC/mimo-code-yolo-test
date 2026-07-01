# 新任务：下面依旧对input_folder的工作，它实际上是一个分类模型的数据集，每个sub_folder其实是一个类别，
# 现在要制作平衡不同类别的数据量制作训练集，注意不要对原数据集做更改，只从中复制图片，
# 具体任务：  对图片数小于100的sub_folder里的图片进行随机的图像增强使样本数到达100；
#             对于图片数大于1000的sub_folder，只随机抽取1000张图片复制到训练集中，注意要随机抽取；
#             抛弃图片数小于一个可调阈值n的sub_folder

import os
import random
import shutil
from PIL import Image, ImageEnhance, ImageOps

def image_augmentation(img_path):
    img = Image.open(img_path)
    img = img.convert("RGB")

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
            print(f'{sub_folder}有类别的数量太少，跳过')
            continue
        elif file_count < 50:
            target_folder = os.path.join(output_folder, sub_folder)
            os.makedirs(target_folder, exist_ok=True)
            
            for file in file_list:
                shutil.copy(os.path.join(sub_folder_path, file), target_folder)
            
            while file_count < 50:
                file_to_augment = random.choice(file_list)
                img = image_augmentation(os.path.join(sub_folder_path, file_to_augment))
                new_file_name = f"{file_to_augment}_augment_{file_count}.jpg"
                img.save(os.path.join(target_folder, new_file_name), quality=100)
                file_count += 1
        elif file_count > 3000:
            target_folder = os.path.join(output_folder, sub_folder)
            os.makedirs(target_folder, exist_ok=True)
            
            sampled_files = random.sample(file_list, 3000)
            for file in sampled_files:
                shutil.copy(os.path.join(sub_folder_path, file), target_folder)
        else:
            target_folder = os.path.join(output_folder, sub_folder)
            os.makedirs(target_folder, exist_ok=True)
            
            for file in file_list:
                shutil.copy(os.path.join(sub_folder_path, file), target_folder)
    
    print("Dataset balancing completed.")

# 设置参数
input_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train0806'
output_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train3000'
threshold_n = 5  # 可调阈值 选择小于该阈值的抛弃

# 运行脚本
balance_dataset(input_folder, output_folder, threshold_n)
