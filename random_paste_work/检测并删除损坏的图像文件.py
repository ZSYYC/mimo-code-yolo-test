import os
from PIL import Image
from tqdm import tqdm

def check_and_remove_corrupt_images(folder_path):
    corrupt_images_count = 0
    image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg") or f.endswith(".png")]

    for filename in tqdm(image_files, desc="Processing images"):
        image_path = os.path.join(folder_path, filename)
        try:
            img = Image.open(image_path)
            img.load()
        except OSError as e:
            print(f"Removing corrupt image {image_path}: {e}")
            os.remove(image_path)
            corrupt_images_count += 1

    return corrupt_images_count

folder_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/招标用数据集20240830/train0806'
folder = os.listdir(folder_path)
for sub_folder in folder:
    sub_folder = os.path.join(folder_path,sub_folder)
    corrupt_images_count = check_and_remove_corrupt_images(sub_folder)
    print(f"Total number of corrupt images removed: {corrupt_images_count}")

