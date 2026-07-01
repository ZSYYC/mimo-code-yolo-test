import os
import random
import shutil

# 假设之前已经抽样的2000张图片存储在之前抽样的文件夹中
previous_sample_folder1 = "/home/yaoteam/yaoteam/wz/测试/抽样图片2及其对应xml/JPGImages/"  # 存储之前已抽样图片的路径
previous_sample_folder2 = "/home/yaoteam/yaoteam/wz/测试/抽样图片及其对应xml/JPGImages/"
previous_sample_folder3 = "/home/yaoteam/yaoteam/wz/测试/抽样图片3及其对应xml/JPGImages/"
total_images_folder = "/home/yaoteam/yaoteam/wz/20250226smallInsect10000/"  # 存储总共有12000张图片的路径
new_sample_folder = "/home/yaoteam/yaoteam/wz/测试/抽样图片4及其对应xml/JPGImages/"  # 存储新抽样图片的路径

# 1. 获取之前已抽样的图片文件名列表
previous_samples1 = set(os.listdir(previous_sample_folder1))  # 使用 set 更高效
previous_samples2 = set(os.listdir(previous_sample_folder2))

# 2. 获取总文件夹中的图片文件名
all_images = os.listdir(total_images_folder)

# 3. 从所有图片中去除之前已抽样的图片
remaining_images = [image for image in all_images if image not in previous_samples1 and image not in previous_samples2]

# 4. 随机抽取2000张图片
new_samples = random.sample(remaining_images, 50)

# 5. 将新抽样的图片复制到指定的文件夹
if not os.path.exists(new_sample_folder):
    os.makedirs(new_sample_folder)

for image in new_samples:
    image_path = os.path.join(total_images_folder, image)
    shutil.copy(image_path, new_sample_folder)

print(f"成功抽取了 {len(new_samples)} 张新图片！")