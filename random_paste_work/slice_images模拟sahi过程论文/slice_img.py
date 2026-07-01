from sahi.slicing import slice_image

import cv2
import os
import re
import numpy as np

def parse_filename(filename):
    """
    Parse the filename to extract coordinates x1, x2, y1, y2
    """
    pattern = r'sliceresult_(\d+)_(\d+)_(\d+)_(\d+)\.png'
    match = re.match(pattern, filename)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        return x1, x2, y1, y2
    else:
        raise ValueError(f"Filename {filename} does not match expected format")

def reconstruct_image(slice_dir, gap, save_path):
    """
    Reconstruct the original image from slices with gaps
    """
    slice_files = [f for f in os.listdir(slice_dir) if f.endswith('.png')]
    
    # Parse the coordinates of each slice
    slices_info = []
    for filename in slice_files:
        x1, x2, y1, y2 = parse_filename(filename)
        slices_info.append((filename, x1, x2, y1, y2))
    
    # Determine the size of the reconstructed image
    max_x = max(info[2] for info in slices_info) + 10*gap# x2
    max_y = max(info[4] for info in slices_info) + 10*gap  # y2
    
    # Create a white background for the reconstructed image
    reconstructed_image = np.ones((max_y + gap, max_x + gap, 3), dtype=np.uint8) * 255 # 255 color
    
    # Paste each slice onto the background
    for filename, x1, x2, y1, y2 in slices_info:
        slice_img = cv2.imread(os.path.join(slice_dir, filename))
        
        # Calculate paste coordinates with gap
        x_paste = x1 + (x1 // 680) * gap 
        if x2 == 5472:#为了处理最后一个图像的gap，680 即x的步进值（因为有重叠）。这里直接填写图像的宽高！！！
            x_paste+=480 # 800+180 - （4000-3520）
        y_paste = y1 + (y1 // 680) * gap
        if y2 == 3648:# 这里直接填写图像的宽高！！！！！
            y_paste+=950       
        # Paste the slice into the reconstructed image
        reconstructed_image[y_paste:y_paste + (y2 - y1), x_paste:x_paste + (x2 - x1)] = slice_img
    
    # Save the final reconstructed image
    cv2.imwrite(save_path, reconstructed_image)

def reconstruct_image_png(slice_dir, gap, save_path):
    """
    Reconstruct the original image from slices with gaps and save with transparent background.
    """
    slice_files = [f for f in os.listdir(slice_dir) if f.endswith('.png')]

    # Parse the coordinates of each slice
    slices_info = []
    for filename in slice_files:
        x1, x2, y1, y2 = parse_filename(filename)
        slices_info.append((filename, x1, x2, y1, y2))

    # Determine the size of the reconstructed image
    max_x = max(info[2] for info in slices_info) + 8 * gap  # x2
    max_y = max(info[4] for info in slices_info) + 6 * gap  # y2

    # Create a transparent background for the reconstructed image (RGBA)
    reconstructed_image = np.zeros((max_y + gap, max_x + gap, 4), dtype=np.uint8)

    # Paste each slice onto the transparent background
    for filename, x1, x2, y1, y2 in slices_info:
        slice_img = cv2.imread(os.path.join(slice_dir, filename), cv2.IMREAD_UNCHANGED)

        # Calculate paste coordinates with gap
        x_paste = x1 + (x1 // 680) * gap
        if x2 == 5472:  # Handle the last image for the x-axis (image width)
            x_paste += 480  # Adjust for the last image's special case
        y_paste = y1 + (y1 // 680) * gap
        if y2 == 3648:  # Handle the last image for the y-axis (image height)
            y_paste += 950

        # Paste the slice into the reconstructed image (including transparency)
        slice_img = cv2.cvtColor(slice_img, cv2.COLOR_BGR2BGRA)  # Convert BGR to BGRA for transparency
        reconstructed_image[y_paste:y_paste + (y2 - y1), x_paste:x_paste + (x2 - x1)] = slice_img

    # Make the white background transparent by setting the alpha channel
    white_pixels = np.all(reconstructed_image[:, :, :3] == [255, 255, 255], axis=-1)
    reconstructed_image[white_pixels] = [0, 0, 0, 0]  # Set white to transparent (R, G, B, A = 0)

    # Save the final reconstructed image as PNG
    cv2.imwrite(save_path, reconstructed_image)

# step 2

if __name__ == "__main__":
    slice_dir = "/home/yaoteam/yaoteam/yyc/random_paste_work/slice_images/slice_result"  # 修改为存放切片图片的目录路径
    gap = 400  # 设置切片之间的空隙大小
    save_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/slice_images/reconstructed_image.png"  # 保存最终还原图像的路径
    
    reconstruct_image_png(slice_dir, gap, save_path)


# step 1

# slice_image_result = slice_image(
#     image='/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/output20241001/0220715_Image_20220715100546085-3-背景.jpg',
#     output_file_name='sliceresult',
#     output_dir='/home/yaoteam/yaoteam/yyc/random_paste_work/slice_images/slice_result',
#     slice_height=800,
#     slice_width=800,
#     overlap_height_ratio=0.15,
#     overlap_width_ratio=0.15,
# )

