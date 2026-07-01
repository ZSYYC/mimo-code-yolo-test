import os
import json
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm
import io

# 检查图像文件是否损坏，使用PIL的Image.open()进行更详细的验证
def check_image_valid(image_path):
    try:
        # 尝试打开图像文件
        with Image.open(image_path) as img:
            img.verify()  # 验证图像文件
        return True
    except (IOError, OSError) as e:
        print(f"Error with image {image_path}: {e}")
        return False


# 删除损坏的图像及其对应的json标注信息
def remove_corrupt_image(image_path, annotations, images, image_id):
    print(f"Removing corrupt image: {image_path}")
    # 删除图像文件
    if os.path.exists(image_path):
        os.remove(image_path)
    # 从annotations中移除对应的标注信息
    annotations = [anno for anno in annotations if anno['image_id'] != image_id]
    # 从images中移除对应的图像信息
    images = [img for img in images if img['id'] != image_id]
    return annotations, images

# 检查所有图像是否损坏
def check_images(image_folder, annotation_file, output_folder=None):
    with open(annotation_file, 'r', encoding='utf-8') as f:
        annotations_data = json.load(f)
    
    annotations = annotations_data['annotations']
    images = annotations_data['images']
    
    # 创建输出目录
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 使用tqdm添加进度条
    for image_info in tqdm(images, desc="Checking images", unit="image"):
        image_path = os.path.join(image_folder, image_info['file_name'])
        image_id = image_info['id']
        
        if not check_image_valid(image_path):
            # 删除损坏的图片及标注信息
            annotations, images = remove_corrupt_image(image_path, annotations, images, image_id)
            # 可以选择将损坏图片复制到output_folder，以便后续检查
            if output_folder:
                os.rename(image_path, os.path.join(output_folder, image_info['file_name']))
    
    # 更新后的annotations数据
    annotations_data['annotations'] = annotations
    annotations_data['images'] = images
    
    # 保存清理后的annotations文件
    with open(annotation_file, 'w', encoding='utf-8') as f:
        json.dump(annotations_data, f)

    print("Image validation completed!")




# 示例：数据集检查
if __name__ == "__main__":
    image_folder = "/home/star/2T/outputs_pesudo_81955/images"  # 图像文件夹路径
    annotation_file = "/home/star/2T/outputs_pesudo_81955/annotations/train2017.json"  # COCO格式的注释文件路径
    output_folder = None  # 可选，损坏图片输出目录
    
    check_images(image_folder, annotation_file, output_folder)
