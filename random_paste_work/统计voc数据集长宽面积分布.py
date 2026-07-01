import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def parse_bboxes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    bboxes = []
    for obj in root.findall('object'):
        xmin = float(obj.find('bndbox/xmin').text)
        ymin = float(obj.find('bndbox/ymin').text)
        xmax = float(obj.find('bndbox/xmax').text)
        ymax = float(obj.find('bndbox/ymax').text)
        bboxes.append((xmin, ymin, xmax, ymax))
    return bboxes

def collect_bbox_statistics(xml_dir):
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    all_bboxes = []

    for xml_file in tqdm(xml_files, desc="Processing XML files"):
        xml_file_path = os.path.join(xml_dir, xml_file)
        bboxes = parse_bboxes(xml_file_path)
        all_bboxes.extend(bboxes)

    return all_bboxes

def plot_bbox_distribution(bboxes, output_dir):
    widths = [bbox[2] - bbox[0] for bbox in bboxes if (bbox[2] - bbox[0]) <= 200]
    heights = [bbox[3] - bbox[1] for bbox in bboxes if (bbox[3] - bbox[1]) <= 200]
    areas = [(bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) for bbox in bboxes if (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) <= 2 * 1e4]

    # 动态设置横坐标范围
    width_bins = np.linspace(0, 200, 200)
    height_bins = np.linspace(0, 200, 200)
    area_bins = np.linspace(0, 2 * 1e4, 200)

    plt.figure(figsize=(12, 8))
    plt.hist(widths, bins=width_bins, color='b', alpha=0.7)
    plt.title('Distribution of BBox Widths')
    plt.xlabel('Width (pixels)')
    plt.ylabel('Count')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'bbox_widths_distribution.png'))
    plt.close()

    plt.figure(figsize=(12, 8))
    plt.hist(heights, bins=height_bins, color='r', alpha=0.7)
    plt.title('Distribution of BBox Heights')
    plt.xlabel('Height (pixels)')
    plt.ylabel('Count')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'bbox_heights_distribution.png'))
    plt.close()

    plt.figure(figsize=(12, 8))
    plt.hist(areas, bins=area_bins, color='g', alpha=0.7)
    plt.title('Distribution of BBox Areas')
    plt.xlabel('Area (pixels^2)')
    plt.ylabel('Count')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'bbox_areas_distribution.png'))
    plt.close()

# 设置路径
xml_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images_for_small_targets_xml'
output_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616'

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 收集坐标框统计信息
bboxes = collect_bbox_statistics(xml_dir)

# 绘制并保存坐标框分布图
plot_bbox_distribution(bboxes, output_dir)
