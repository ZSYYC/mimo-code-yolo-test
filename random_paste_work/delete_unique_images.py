import os

def delete_unique_images(folder_to_check, reference_folder):
    # 获取参考文件夹中所有图片的文件名
    reference_images = set(os.listdir(reference_folder))

    # 获取要检查的文件夹中所有图片的文件名
    images_to_check = os.listdir(folder_to_check)

    # 遍历要检查的文件夹中的图片
    for image in images_to_check:
        # 如果图片不在参考文件夹中，删除它
        if image not in reference_images:
            image_path = os.path.join(folder_to_check, image)
            os.remove(image_path)
            print(f"Deleted {image_path}")

# 示例用法
folder_to_check = '/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_bbfshfsyechan/bbfs'
reference_folder = 'path_to_reference_folder'

delete_unique_images(folder_to_check, reference_folder)
