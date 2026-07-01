import cv2
import os

def convert_png_to_jpg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            png_path = os.path.join(input_folder, filename)
            img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)  # 读取图片，包括 alpha 通道

            # 检查图片是否具有透明度
            if img.shape[2] == 4:  # 有 alpha 通道
                # 分离 BGR 和 alpha 通道
                bgr = img[:, :, :3]
                # 直接丢弃 alpha 通道
                img = bgr
            else:
                # 如果没有 alpha 通道，直接使用 BGR 图像
                img = img[:, :, :3]

            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            jpg_path = os.path.join(output_folder, jpg_filename)

            # 保存为 JPEG 格式，并设置质量参数为 95（接近无损）
            cv2.imwrite(jpg_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

# 示例用法
input_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_cebaodeng2023all_insect'
output_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/crop_output_cebaodeng2023all_insect_putong'
convert_png_to_jpg(input_folder, output_folder)
