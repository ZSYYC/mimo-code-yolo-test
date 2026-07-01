import os
from PIL import Image


def is_corrupted(image_path):
    """尝试打开图片，如果失败则返回 True（图片损坏）"""
    try:
        with Image.open(image_path) as img:
            img.verify()  # 只验证图片完整性，不加载图像
        return False
    except Exception as e:
        print(f"❌ 损坏的图片: {image_path}，错误: {e}")
        return True


def check_images_in_directory(directory):
    """遍历目录中的所有图片文件，检测是否有损坏"""
    corrupted_images = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):  # 只检查常见图片格式
                if is_corrupted(file_path):
                    corrupted_images.append(file_path)

    if corrupted_images:
        print("\n🚨 发现损坏的图片：")
        for img in corrupted_images:
            print(img)
    else:
        print("\n✅ 没有发现损坏的图片！")


# 设置需要检查的文件夹路径
directory_path = "/home/yaoteam/yaoteam/wz/飞虱叶蝉数据集/train/"  # 请替换成实际路径
check_images_in_directory(directory_path)