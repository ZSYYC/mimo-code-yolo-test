import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from PIL import Image

def parse_xml_annotations(xml_folder, image_folder):
    resolutions = []
    areas_ratios = []

    for xml_file in os.listdir(xml_folder):
        if not xml_file.endswith('.xml'):
            continue
        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Get image dimensions
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        resolution = (width, height)
        resolutions.append(resolution)

        # Calculate area ratios for all objects in the image
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            bbox_area = (xmax - xmin) * (ymax - ymin)
            img_area = width * height
            areas_ratios.append(bbox_area / img_area)

    return resolutions, areas_ratios

def plot_resolution_distribution(resolutions):
    # Count resolution frequencies
    resolution_counts = Counter(resolutions)
    resolutions, counts = zip(*resolution_counts.items())
    resolution_labels = [f"{res[0]}x{res[1]}" for res in resolutions]

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(resolution_labels, counts, color='steelblue')
    plt.xlabel('Image Resolution', fontsize=18, fontname='Times New Roman')
    plt.ylabel('Number of Images', fontsize=18, fontname='Times New Roman')
    # plt.title('Image Resolution Distribution', fontsize=21, fontname='Times New Roman')
    # plt.xticks(rotation=15, ha='right', fontsize=15, fontname='Times New Roman')
    plt.xticks(fontsize=15, fontname='Times New Roman')
    plt.yticks(fontsize=15, fontname='Times New Roman')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/home/yaoteam/yaoteam/yyc/random_paste_work/小论文统计灯诱昆虫数据集分辨率/resolution_distribution.png', dpi=300)
    # plt.show()

def plot_area_ratio_distribution(area_ratios):
    # 转换为百分比
    area_ratios_percent = [r * 100 for r in area_ratios]  # 将比例转换为百分比
    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(
        area_ratios_percent,
        bins=np.linspace(0, 5, 40),  # Adjusted range to [0, 0.2]
        color='coral',
        edgecolor='black',
        alpha=0.7
    )
    plt.xlabel('Relative Area Ratio (%)', fontsize=18, fontname='Times New Roman')
    plt.ylabel('Frequency', fontsize=18, fontname='Times New Roman')
    # plt.title('Insect Area Ratio Distribution', fontsize=21, fontname='Times New Roman')
    plt.xticks(fontsize=15, fontname='Times New Roman')
    plt.yticks(fontsize=15, fontname='Times New Roman')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/home/yaoteam/yaoteam/yyc/random_paste_work/小论文统计灯诱昆虫数据集分辨率/area_ratio_distribution.png', dpi=300)
    # plt.show()

def plot_insect_count_distribution(xml_folder):
    # 统计每张图片上的昆虫个数
    insect_counts = []
    for xml_file in os.listdir(xml_folder):
        if not xml_file.endswith('.xml'):
            continue
        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 统计该文件中所有object的数量
        insect_count = len(root.findall('object'))
        insect_counts.append(insect_count)

    # 显示昆虫个数分布的柱状图
    plt.figure(figsize=(10, 6))
    plt.hist(
        insect_counts,
        bins=np.arange(0, max(insect_counts) + 2) - 0.5,  # 设置柱宽，确保整数对齐
        color='seagreen',
        edgecolor='black',
        alpha=0.7
    )
    plt.xlabel('Number of Insects per Image', fontsize=18, fontname='Times New Roman')
    plt.ylabel('Number of Images', fontsize=18, fontname='Times New Roman')
    # plt.title('Insect Count Distribution per Image', fontsize=21, fontname='Times New Roman')
    plt.xticks(fontsize=15, fontname='Times New Roman')
    plt.yticks(fontsize=15, fontname='Times New Roman')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/home/yaoteam/yaoteam/yyc/random_paste_work/小论文统计灯诱昆虫数据集分辨率/insect_count_distribution.png', dpi=300)
    # plt.show()
    
def plot_class_distribution(dataset_path):
    # 获取每个类别文件夹下的图片数量
    class_counts = {}
    for class_name in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_path):
            image_count = len([img for img in os.listdir(class_path) if img.endswith(('.jpg', '.png', '.jpeg'))])
            class_counts[class_name] = image_count

    # 将类别按照数量降序排序
    sorted_counts = sorted(class_counts.values(), reverse=True)  # 只保留数量
    sorted_counts = sorted_counts[:237]  # 只保留前 237 类

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.bar(
        range(len(sorted_counts)),
        sorted_counts,
        color='skyblue',
        edgecolor='black',
        alpha=0.8
    )

    # 设置横坐标和标题
    plt.xlabel('Class Index (Top 237)', fontsize=18, fontname='Times New Roman')
    plt.ylabel('Frequency', fontsize=18, fontname='Times New Roman')
    # plt.title('Class Distribution (Top 237)', fontsize=21, fontname='Times New Roman')

    # 设置横坐标刻度间隔，显示从 0 到 236 的指定刻度
    plt.xticks(
        ticks=np.linspace(0, 236, 10),
        labels=[f"{int(x)}" for x in np.linspace(0, 236, 10)],
        fontsize=12,
        fontname='Times New Roman'
    )
    plt.yticks(fontsize=12, fontname='Times New Roman')

    # 添加网格
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 保存图片
    plt.savefig('/home/yaoteam/yaoteam/yyc/random_paste_work/小论文统计灯诱昆虫数据集分辨率/class_distribution.png', dpi=300)
    # plt.show()

if __name__ == "__main__":
    # Paths to XML annotations and image folder
    xml_folder = "/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/xml汇总"
    image_folder = "/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images"
    # 分类数据集路径
    dataset_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train0806"
    # Parse data
    resolutions, area_ratios = parse_xml_annotations(xml_folder, image_folder)

    # Plot distributions
    plot_resolution_distribution(resolutions)
    plot_area_ratio_distribution(area_ratios)
    plot_insect_count_distribution(xml_folder)  # 绘制昆虫个数分布图
    # 绘制类别分布图
    plot_class_distribution(dataset_path)
