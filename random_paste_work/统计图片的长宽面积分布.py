import os
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size  # Returns (width, height)

def plot_and_save(data, title, xlabel, ylabel, save_path):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=50, alpha=0.75, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

def analyze_image_folder(folder_path, save_dir,save_img_tag):
    widths = []
    heights = []
    areas = []
    aspect_ratios = []
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    image_files = [os.path.join(root, file)
                   for root, dirs, files in os.walk(folder_path)
                   for file in files
                   if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'))]

    for image_path in tqdm(image_files, desc="Processing images"):
        width, height = get_image_dimensions(image_path)
        area = width * height
        aspect_ratio = height / width
        widths.append(width)
        heights.append(height)
        areas.append(area)
        aspect_ratios.append(aspect_ratio)
    
    plot_and_save(widths, 'Width Distribution', 'Width (pixels)', 'Frequency', os.path.join(save_dir, f'{save_img_tag}_width_distribution.png'))
    plot_and_save(heights, 'Height Distribution', 'Height (pixels)', 'Frequency', os.path.join(save_dir, f'{save_img_tag}_height_distribution.png'))
    plot_and_save(areas, 'Area Distribution', 'Area (pixels^2)', 'Frequency', os.path.join(save_dir, f'{save_img_tag}_area_distribution.png'))
    plot_and_save(aspect_ratios, 'Aspect Ratio Distribution', 'Aspect Ratio (Width/Height)', 'Frequency', os.path.join(save_dir, f'{save_img_tag}_aspect_ratio_distribution.png'))


# Example usage:
folder_path = '/home/yaoteam/yaoteam/wz/20250226smallInsect10000/'
save_dir = '/home/yaoteam/yaoteam/wz/小虫数据集分布/'
save_img_tag = 'y2'
analyze_image_folder(folder_path, save_dir,save_img_tag)
