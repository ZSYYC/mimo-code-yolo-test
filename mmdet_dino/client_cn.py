import argparse
import os
import random
import grpc
import detect_model_pb2
import detect_model_pb2_grpc
import cv2
import time
import csv
from tqdm import tqdm  # 进度条库
import numpy as np
from PIL import Image, ImageDraw, ImageFont  # 用于支持中文字体
# server address
SERVER_ADDRESS = "192.168.1.224:40051"
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024

# CSV文件读取,用于英文标签和中文名之间的转换,xml文件用英文标签,可视化使用中文名
result_dict = {}
with open('/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi_260105.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        key = row[1]  # 第二列
        value = row[3]  # 第四列
        result_dict[key] = value

reversed_dict = {value: key for key, value in result_dict.items()}

# 生成唯一颜色的函数
def generate_unique_color(name):
    """ 根据类别名称生成唯一的 RGB 颜色 """
    random.seed(hash(name))  # 根据标签名设置随机种子
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

def calculate_brightness(color):
    """根据RGB颜色计算亮度"""
    r, g, b = color
    return 0.299 * r + 0.587 * g + 0.114 * b

def get_contrasting_font_color(bg_color):
    """根据背景颜色选择对比度最大的字体颜色（黑或白）"""
    brightness = calculate_brightness(bg_color)
    return (0, 0, 0) if brightness > 128 else (255, 255, 255)

def get_name(label):
    """ 根据标签返回中文名称 """
    return reversed_dict.get(label, label)

def get_label(name):
    """ 根据名称返回标签 """
    return result_dict.get(name, name)

def visualize_detection(image_path, detected_objects, output_path):
    """ 在图像上绘制目标检测的边界框和标签 """

    # 读取图像并在OpenCV中绘制边界框
    image = cv2.imread(image_path)

    # 解析detected_objects的字段
    fields = detected_objects.ListFields()
    tags, corners, accuracies = [], [], []

    for field, value in fields:
        if field.name == "tag":
            tags = value
        elif field.name == "corner":
            corners = value
        elif field.name == "accuracy":
            accuracies = value

    if len(tags) == len(corners) == len(accuracies):
        for i in range(len(tags)):
            tag = get_name(tags[i])  # 你自定义的标签名称处理函数
            corner = corners[i]
            accuracy = accuracies[i]

            x1, y1, x2, y2 = corner.x1, corner.y1, corner.x2, corner.y2
            # 生成唯一的背景颜色
            bg_color = generate_unique_color(tag)  # 使用标签名称生成颜色
            border_color = bg_color  # 边界框的颜色和背景颜色一致

            # 计算与背景对比的字体颜色
            font_color = get_contrasting_font_color(bg_color)
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), border_color, 5)

    # 将OpenCV图像转换为PIL图像，开始绘制标签
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    font_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/simhei.ttf'  # 请确保simhei.ttf路径正确
    font_size = 20  # 字体大小
    font = ImageFont.truetype(font_path, font_size)

    if len(tags) == len(corners) == len(accuracies):
        for i in range(len(tags)):
            tag = get_name(tags[i])  # 你自定义的标签名称处理函数
            corner = corners[i]
            accuracy = accuracies[i]

            x1, y1, x2, y2 = corner.x1, corner.y1, corner.x2, corner.y2

            label = f"{tag}: {accuracy:.2f}"

            # 计算标签的宽度和高度
            text_width, text_height = font.getbbox(label)[2:4]  # 获取标签的宽和高
            label_y = max(y1, text_height + 1)

            # 生成唯一的背景颜色
            bg_color = generate_unique_color(tag)  # 标签背景颜色
            font_color = get_contrasting_font_color(bg_color)  # 字体颜色
            border_color = bg_color  # 边界框的颜色和背景颜色一致

            # 绘制标签背景
            draw.rectangle(
                [(int(x1), int(label_y) - text_height - 1), 
                 (int(x1) + text_width, int(label_y) + 1)], 
                fill=bg_color
            )
            
            # 绘制中文标签
            draw.text((int(x1), int(label_y) - text_height - 0.5), label, font=font, fill=font_color)

    # 将PIL图像转换回OpenCV图像
    image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    # 保存图像
    cv2.imwrite(output_path, image)

def parse_args():
    """ 解析命令行参数 """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img260413', help='Path to the image directory')
    # parser.add_argument('--path', type=str, default='/home/yaoteam/yaoteam/yyc/mmdet_dino/依科曼摆拍实拍图片', help='Path to the image directory')
    parser.add_argument('--sample_ratio', type=float, default=1, help='Sampling ratio for images (0.0-1.0)')
    return parser.parse_args()

def detect_objects(stub, image_path, image_name):
    """ 发送图像数据到服务器进行检测 """
    # print(f'Estimating image: ' + os.path.join(image_path, image_name))
    with open(os.path.join(image_path, image_name), 'rb') as fp:
        image_bytes = fp.read()
    return stub.detect(detect_model_pb2.Image(img_name=image_name, data=image_bytes))

def result_is_not_empty(detected_objects):
    fields = detected_objects.ListFields()
    isEmpty = True
    for field, value in fields:
        if field.name == "tag":
            isEmpty = False
        elif field.name == "corner":
            isEmpty = False
    return  isEmpty


def main():
    args = parse_args()
    image_path = args.path
    sample_ratio = args.sample_ratio
    target = SERVER_ADDRESS
    output_path = "/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img260413_output"
    # output_path = "/home/yaoteam/yaoteam/yyc/mmdet_dino/tmp_output"
    os.makedirs(output_path, exist_ok=True)
    
    with grpc.insecure_channel(target, options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
    ]) as channel:

        stub = detect_model_pb2_grpc.DetectModelStub(channel)
        try:
            image_name_list = os.listdir(image_path)
            
            if sample_ratio < 1.0:
                sample_size = int(len(image_name_list) * sample_ratio)
                image_name_list = random.sample(image_name_list, sample_size)

            for image_name in tqdm(image_name_list, desc="Processing images"):
                detected_objects = detect_objects(stub, image_path, image_name)
                if result_is_not_empty(detected_objects): # 如果是没有目标的图像则跳过
                    continue
                visualize_detection(os.path.join(image_path, image_name), detected_objects, os.path.join(output_path, image_name))
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print('\n耗时：', time.perf_counter() - start, 's')
