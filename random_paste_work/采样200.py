import os
import shutil
import random

# 🔹 原始数据集所在路径（需要修改为你的数据集路径）
source_root = "/home/yaoteam/yaoteam/wz/测试/裁剪出多类别小图/"  # 你的数据集根目录
# 🔹 新的抽样数据集路径
target_root = "/home/yaoteam/yaoteam/wz/测试/测试集2/"

# 🔹 每个类别抽取 200 张图片
num_samples = 200

# 创建目标文件夹
os.makedirs(target_root, exist_ok=True)

# 遍历所有类别文件夹
for class_name in os.listdir(source_root):
    class_path = os.path.join(source_root, class_name)  # 类别文件夹路径

    # 确保是文件夹
    if not os.path.isdir(class_path):
        continue

        # 获取所有图片文件
    images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    # 如果图片数量不足 200，取全部，否则随机采样 200 张
    sampled_images = random.sample(images, min(num_samples, len(images)))

    # 🔹 创建目标类别文件夹
    target_class_path = os.path.join(target_root, class_name)
    os.makedirs(target_class_path, exist_ok=True)

    # 复制选中的图片到新的文件夹
    for img in sampled_images:
        src_img_path = os.path.join(class_path, img)
        dst_img_path = os.path.join(target_class_path, img)
        shutil.copy(src_img_path, dst_img_path)  # 复制文件

    print(f"📌 类别 [{class_name}] 采样完成，共 {len(sampled_images)} 张图片")

print("✅ 所有类别的图片采样完成！")