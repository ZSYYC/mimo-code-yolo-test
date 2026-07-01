import os
import cv2
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

# 参数
image_folder = '/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/img'  # VOC数据集图片文件夹路径
xml_folder = '/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/xml'  # VOC数据集XML标注文件夹路径

# 获取类别名称
classes = {}  # 存储每个类别的实例列表
class_names = []

# 遍历xml文件，统计每个类别的实例数量
def parse_annotations():
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            # 获取图像文件名
            image_name = root.find('filename').text
            image_path = os.path.join(image_folder, image_name)
            # 遍历所有object标签
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                if class_name not in classes:
                    classes[class_name] = []
                classes[class_name].append(image_path)

# 从每个类别的第一张图片中裁剪目标并保存
def crop_objects():
    cropped_images = {}
    for class_name, images in classes.items():
        cropped_images[class_name] = []
        # 只选取每个类别的第一张图片进行处理
        selected_image_path = images[0]
        # 读取图片
        image = cv2.imread(selected_image_path)
        # 解析xml文件来获取目标位置
        xml_path = os.path.join(xml_folder, os.path.basename(selected_image_path).replace('.bmp', '.xml')) # .jpg
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for obj in root.findall('object'):
            if obj.find('name').text == class_name:
                # 获取bounding box
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                # 裁剪目标区域
                cropped = image[ymin:ymax, xmin:xmax]
                cropped_images[class_name].append(cropped)
    return cropped_images

# 自适应大小填充白色背景
def resize_with_padding(image, target_size=(100, 100)):
    h, w = image.shape[:2]
    target_h, target_w = target_size

    # 计算长宽的缩放比例
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # 调整图像大小，保持长宽比例
    resized_image = cv2.resize(image, (new_w, new_h))

    # 计算填充的大小
    top = (target_h - new_h) // 2
    bottom = target_h - new_h - top
    left = (target_w - new_w) // 2
    right = target_w - new_w - left

    # 填充白色背景
    padded_image = cv2.copyMakeBorder(resized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    return padded_image

# 可视化类别图像并保存
def visualize_cropped_images(cropped_images):
    # 获取总图像数量
    total_images = sum(len(images) for images in cropped_images.values())
    
    if total_images == 0:
        print("No cropped images to visualize.")
        return
    
    # 计算需要的行和列数，确保每行最多10个图像
    max_images_per_row = 10
    rows = (total_images + max_images_per_row - 1) // max_images_per_row  # 向上取整
    columns = min(max_images_per_row, total_images)

    # 创建画布，动态调整画布大小
    fig, axes = plt.subplots(rows, columns, figsize=(columns * 2, rows * 2))
    axes = axes.flatten()

    # 填充每个位置
    idx = 0
    for class_name, images in cropped_images.items():
        if len(images) > 0:
            image = images[0]  # 只取每个类别的第一张图像
            # 调整图片大小并保持长宽比例
            image_resized = resize_with_padding(image, target_size=(100, 100))
            # 获取类别数量
            class_count = len(classes[class_name])
            # 显示图片并添加标签，标签为 类别:数量
            ax = axes[idx]
            ax.imshow(cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB))
            ax.set_title(f"{class_name}: {class_count}", fontsize=8)
            ax.axis('off')
            idx += 1

    # 删除多余的子图
    for i in range(idx, len(axes)):
        axes[i].axis('off')

    # 调整子图之间的间距
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.savefig('/home/star/2T/yyc/2024拍摄测报灯招标图像数据集/visualized_output.png', dpi=300)
    plt.close()

# 统计每个类别的数量并输出
def print_class_counts():
    print("Class counts:")
    for class_name, images in classes.items():
        print(f"{class_name}: {len(images)}")

# 主程序
def main():
    parse_annotations()
    print_class_counts()
    cropped_images = crop_objects()
    visualize_cropped_images(cropped_images)

if __name__ == "__main__":
    main()
