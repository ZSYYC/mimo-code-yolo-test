import os
import argparse
import random
from PIL import Image
import math
#任务：给定图片文件夹路径，输出为一张图片，该图片上抽样排列展示图片文件夹中的缩略图，每行排列的图片数量可设置，图片间隙可设置，排列拼接完成后的输出图分辨率可设置，缩略图分辨率自适应。

def create_thumbnail_grid(input_folder, output_path, images_per_row=5, gap=10, output_width=1920, sample_count=None):
    """
    创建图片缩略图网格

    参数:
        input_folder: 输入图片文件夹路径
        output_path: 输出图片路径
        images_per_row: 每行图片数量
        gap: 图片间隙(像素)
        output_width: 输出图片宽度(像素)
        sample_count: 要抽样的图片数量，None表示使用所有图片
    """
    # 支持的图片格式
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']

    # 获取所有图片文件
    image_files = []
    for file in os.listdir(input_folder):
        ext = os.path.splitext(file)[1].lower()
        if ext in supported_formats:
            image_files.append(os.path.join(input_folder, file))

    if not image_files:
        print(f"在 {input_folder} 中没有找到图片文件")
        return
    
    if sample_count is not None and sample_count < len(image_files):
        print(f"从 {len(image_files)} 张图片中随机抽样 {sample_count} 张")
        image_files = random.sample(image_files, sample_count)
    else:
        print(f"使用文件夹中的所有 {len(image_files)} 张图片")

    # 计算缩略图尺寸
    available_width = output_width - (gap * (images_per_row + 1))
    thumbnail_width = available_width // images_per_row

    # 加载所有图片并创建缩略图
    thumbnails = []
    for img_path in image_files:
        try:
            img = Image.open(img_path)
            # 计算等比例缩放后的高度
            aspect_ratio = img.height / img.width
            thumbnail_height = int(thumbnail_width * aspect_ratio)
            # 创建缩略图
            img_thumbnail = img.resize((thumbnail_width, thumbnail_height), Image.LANCZOS)
            thumbnails.append(img_thumbnail)
        except Exception as e:
            print(f"处理图片 {img_path} 时出错: {e}")

    # 计算行数
    num_rows = math.ceil(len(thumbnails) / images_per_row)

    # 计算每行的高度
    row_heights = []
    for i in range(num_rows):
        start_idx = i * images_per_row
        end_idx = min(start_idx + images_per_row, len(thumbnails))
        row_images = thumbnails[start_idx:end_idx]
        if row_images:
            max_height = max(img.height for img in row_images)
            row_heights.append(max_height)

    # 计算输出图片的总高度
    total_height = sum(row_heights) + gap * (num_rows + 1)

    # 创建输出图片
    output_img = Image.new('RGB', (output_width, total_height), (255, 255, 255))

    # 放置缩略图
    y_offset = gap
    for i in range(num_rows):
        x_offset = gap
        start_idx = i * images_per_row
        end_idx = min(start_idx + images_per_row, len(thumbnails))
        row_images = thumbnails[start_idx:end_idx]

        for img in row_images:
            output_img.paste(img, (x_offset, y_offset))
            x_offset += img.width + gap

        y_offset += row_heights[i] + gap

    # 保存输出图片
    output_img.save(output_path)
    print(f"缩略图网格已保存至 {output_path}")
    print(f"总共处理了 {len(thumbnails)} 张图片")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建图片缩略图网格")
    parser.add_argument("--input_folder", default="/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images")
    parser.add_argument("--output_path", default="/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/数据集缩略图展示1000.jpg")
    parser.add_argument("--images_per_row", type=int, default=50, help="每行图片数量")
    parser.add_argument("--gap", type=int, default=1, help="图片间隙(像素)")
    parser.add_argument("--output_width", type=int, default=5000, help="输出图片宽度(像素)")
    parser.add_argument("--sample_count", type=int, default=1000, help="要抽样的图片数量，默认使用所有图片")  # 新增参数

    args = parser.parse_args()

    create_thumbnail_grid(
        args.input_folder,
        args.output_path,
        args.images_per_row,
        args.gap,
        args.output_width,
        args.sample_count
    )