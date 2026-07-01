import os
import glob
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns

# 设置 seaborn 样式
sns.set(style="darkgrid")

# 配置 XML 文件夹路径和保存图片的路径（请修改为你的路径）
xml_folder = "/home/yaoteam/yaoteam/wz/20250303_preds2coco_xml_已过滤/"  # 替换为你的 XML 文件夹路径
save_path = "/home/yaoteam/yaoteam/wz/检测框面积分布_已过滤/"  # 替换为你想存储图像的文件夹路径
os.makedirs(save_path, exist_ok=True)  # 如果文件夹不存在，则创建

# 用于存储 bbox 相关数据的列表
widths = []
heights = []
areas = []
ratios = []

# 解析 XML 文件
def parse_voc_xml(file_path):
    """解析 VOC 格式的 XML 文件，提取 bounding box 数据"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for obj in root.findall("object"):
        bbox = obj.find("bndbox")
        xmin = int(float(bbox.find("xmin").text))
        ymin = int(float(bbox.find("ymin").text))
        xmax = int(float(bbox.find("xmax").text))
        ymax = int(float(bbox.find("ymax").text))
        
        width = xmax - xmin
        height = ymax - ymin
        area = width * height
        ratio = width / height if height != 0 else 0  # 避免除以 0
        
        widths.append(width)
        heights.append(height)
        areas.append(area)
        ratios.append(ratio)

# 遍历所有 XML 文件
xml_files = glob.glob(os.path.join(xml_folder, "*.xml"))
for xml_file in xml_files:
    parse_voc_xml(xml_file)

# 绘制数据分布图并保存
def plot_and_save_distribution(data, title, xlabel, filename, ylabel="Frequency", bins=30):
    """绘制直方图并保存到文件"""
    plt.figure(figsize=(8, 5))
    sns.histplot(data, bins=bins, kde=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # 限制 X 轴的范围到 0 - 200000
    #plt.xlim(0, 0.5e5)  # 限制 X 轴范围
    
    # 保存图像
    save_file = os.path.join(save_path, filename)
    plt.savefig(save_file, dpi=300, bbox_inches='tight')  # dpi=300 提高分辨率
    print(f"图像已保存：{save_file}")
    
    plt.close()  # 关闭图像，避免占用过多内存

# 生成并保存四个分布图
plot_and_save_distribution(widths, "Bounding Box 宽度分布", "Width", "width_distribution.png")
plot_and_save_distribution(heights, "Bounding Box 高度分布", "Height", "height_distribution.png")
plot_and_save_distribution(areas, "Bounding Box 面积分布", "Area", "area_distribution.png")
plot_and_save_distribution(ratios, "Bounding Box 长宽比分布", "Aspect Ratio", "ratio_distribution.png")