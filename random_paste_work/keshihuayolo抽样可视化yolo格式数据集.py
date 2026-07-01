import os
import random
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

def load_yolo_labels(txt_file):
    """加载 YOLO 格式的标注信息"""
    with open(txt_file, 'r') as f:
        labels = f.readlines()
    annotations = []
    for label in labels:
        parts = label.strip().split()
        cls_id, x_center, y_center, width, height = map(float, parts)
        annotations.append((cls_id, x_center, y_center, width, height))
    return annotations

def draw_yolo_boxes(image, annotations, class_names=None):
    """在图像上绘制 YOLO 格式的目标框"""
    h, w, _ = image.shape
    for annotation in annotations:
        cls_id, x_center, y_center, box_width, box_height = annotation
        x1 = int((x_center - box_width / 2) * w)
        y1 = int((y_center - box_height / 2) * h)
        x2 = int((x_center + box_width / 2) * w)
        y2 = int((y_center + box_height / 2) * h)
        label = str(int(cls_id)) if class_names is None else class_names[int(cls_id)]
        color = (0, 255, 0)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

def visualize_yolo_dataset(images_dir, labels_dir, sample_size, output_dir, class_names=None):
    """随机抽样并保存可视化 YOLO 数据集"""
    # 获取所有图像文件和标注文件
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    label_files = [f.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt') for f in image_files]

    # 随机抽样
    sampled_indices = random.sample(range(len(image_files)), min(sample_size, len(image_files)))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx in tqdm(sampled_indices, desc="Visualizing Samples"):
        image_path = os.path.join(images_dir, image_files[idx])
        label_path = os.path.join(labels_dir, label_files[idx])

        if not os.path.exists(image_path) or not os.path.exists(label_path):
            print(f"Missing file: {image_path} or {label_path}")
            continue

        # 加载图像和标注
        image = cv2.imread(image_path)
        annotations = load_yolo_labels(label_path)

        # 绘制目标框
        image_with_boxes = draw_yolo_boxes(image, annotations, class_names)

        # 保存可视化结果
        output_path = os.path.join(output_dir, image_files[idx])
        cv2.imwrite(output_path, image_with_boxes)

if __name__ == "__main__":
    # 输入图片路径和标注路径
    images_directory = "/home/yaoteam/yaoteam/yyc/random_paste_work/Rice_dataset/test/images"
    labels_directory = "/home/yaoteam/yaoteam/yyc/random_paste_work/Rice_dataset/test/labels"

    # 指定随机抽样的数量
    sample_count = 20

    # 指定输出目录
    output_directory = "/home/yaoteam/yaoteam/yyc/random_paste_work/Rice_dataset/可视化/test"

    # 如果有类别名称列表，可提供
    class_names_list = None  # 或者例如 ["cat", "dog", "car"]

    visualize_yolo_dataset(images_directory, labels_directory, sample_count, output_directory, class_names_list)
