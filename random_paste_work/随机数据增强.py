import cv2
import numpy as np
import albumentations as A
import random
import os


# 1. 定义数据增强的变换
def get_augmentation():
    return A.Compose([
        A.RandomCrop(width=224, height=224, p=0.5),  # 随机裁剪
        A.HorizontalFlip(p=0.5),  # 随机水平翻转
        A.VerticalFlip(p=0.2),  # 随机垂直翻转
        A.Rotate(limit=30, p=0.5),  # 随机旋转 -30~30 度
        A.RandomBrightnessContrast(p=0.5),  # 随机亮度对比度
        A.GaussianBlur(blur_limit=(3, 7), p=0.3),  # 随机高斯模糊
        A.HueSaturationValue(p=0.5),  # 调整色相、饱和度
        A.ISONoise(p=0.3),  # 添加ISO噪声
        A.CoarseDropout(max_holes=8, max_height=16, max_width=16, p=0.3),  # 随机遮挡
    ])


# 2. 处理单张图片
def augment_image(image_path, save_path, num_aug=5):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV 读取的是 BGR，需要转换成 RGB

    # 获取数据增强器
    augmenter = get_augmentation()

    for i in range(num_aug):
        augmented = augmenter(image=image)["image"]  # 进行数据增强
        augmented = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)  # 还原成 BGR 格式

        # 生成新的文件名
        base_name = os.path.basename(image_path).split('.')[0]
        new_file = os.path.join(save_path, f"{base_name}_aug_{i}.jpg")

        # 保存增强后的图片
        cv2.imwrite(new_file, augmented)


# 3. 处理整个文件夹
def augment_dataset(input_folder, output_folder, num_aug=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

    for img_file in image_files:
        image_path = os.path.join(input_folder, img_file)
        augment_image(image_path, output_folder, num_aug)


# 示例：对 `input_images/` 文件夹内的图片进行增强，并保存到 `augmented_images/`
input_folder = "/home/yaoteam/yaoteam/wz/测试/裁剪出多类别小图/双斑痕叶蝉/"
output_folder = "/home/yaoteam/yaoteam/wz/测试/裁剪出多类别小图/双斑痕叶蝉/"
augment_dataset(input_folder, output_folder, num_aug=3)

print("数据增强完成！")