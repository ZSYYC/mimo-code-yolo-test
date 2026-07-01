import os
from PIL import Image, UnidentifiedImageError

def delete_corrupted_images(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # 尝试打开图像文件
                img = Image.open(file_path)
                img.verify()  # 验证图像文件
            except (UnidentifiedImageError, OSError) as e:
                # 如果捕获到UnidentifiedImageError或OSError，表示图像文件损坏
                print(f"Deleting corrupted image: {file_path} - {e}")
                os.remove(file_path)
            except Exception as e:
                # 处理其他可能的异常
                print(f"Error processing image: {file_path} - {e}")

# 要处理的根目录
root_directory = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train3000/val'

# 调用函数删除损坏的图片文件
delete_corrupted_images(root_directory)
