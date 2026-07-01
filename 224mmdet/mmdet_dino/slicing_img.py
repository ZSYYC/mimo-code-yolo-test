from sahi.slicing import slice_image
import os
from tqdm import tqdm

# 定义输入和输出文件夹路径
input_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/data/val_img_cebaodeng/images'
output_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/data/val_img_cebaodeng_sliced/images'

# 获取输入文件夹中所有的图片文件
image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

# 使用tqdm显示进度条
for filename in tqdm(image_files, desc='slicing images'):
    # 构造输入图片的完整路径
    image_path = os.path.join(input_dir, filename)
    
    # 构造输出图片的文件名，使用原始图片文件名作为输出文件名
    output_filename = os.path.splitext(filename)[0] + '_'
    
    # 调用slice_image函数进行切分
    slice_image_result = slice_image(
        image=image_path,
        output_file_name=output_filename,
        output_dir=output_dir,
        slice_height=1600,
        slice_width=2666,
        overlap_height_ratio=0.25,
        overlap_width_ratio=0.25,
    )
