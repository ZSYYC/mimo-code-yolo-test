import argparse
import os
import grpc

import detect_model_pb2
import detect_model_pb2_grpc
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import xml.etree.ElementTree as ET
# server address
# SERVER_ADDRESS = "192.168.1.216:9222"
# SERVER_ADDRESS = "192.168.1.222:50052" # 小虫体模型
SERVER_ADDRESS = "192.168.1.222:50055" # 测报灯模型小虫
# max message length: 256MB
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024

import cv2


def visualize_detection_and_xml(image_path, detected_objects, output_path):
    # 读取图像
    image = cv2.imread(image_path)
    h, w, c = image.shape

    # 使用 ListFields 获取字段值
    fields = detected_objects.ListFields()
    tags, corners, accuracies = [], [], []

    for field, value in fields:
        if field.name == "tag":
            tags = value
        elif field.name == "corner":
            corners = value
        elif field.name == "accuracy":
            accuracies = value

    # 构建 VOC XML 根节点
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "filename").text = os.path.basename(output_path)
    
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(w)
    ET.SubElement(size, "height").text = str(h)
    ET.SubElement(size, "depth").text = str(c)

    # 检测可视化 + XML写入
    if len(tags) == len(corners) == len(accuracies):
        for tag, corner, accuracy in zip(tags, corners, accuracies):
            x1, y1, x2, y2 = int(corner.x1), int(corner.y1), int(corner.x2), int(corner.y2)

            # 绘制矩形
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 5)

            # 标签绘制
            label = f"{tag}: {accuracy:.2f}"
            font_scale = 2
            font_thickness = 3
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            label_y = max(y1, label_size[1] + 10)

            cv2.rectangle(
                image,
                (x1, label_y - label_size[1] - 10),
                (x1 + label_size[0], label_y + 10),
                (0, 255, 0),
                cv2.FILLED
            )
            cv2.putText(
                image, label, (x1, label_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, (0, 0, 0), font_thickness
            )

            # 写入 VOC XML object 字段
            obj = ET.SubElement(annotation, "object")
            ET.SubElement(obj, "name").text = str(tag)
            ET.SubElement(obj, "difficult").text = "0"
            bndbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(x1)
            ET.SubElement(bndbox, "ymin").text = str(y1)
            ET.SubElement(bndbox, "xmax").text = str(x2)
            ET.SubElement(bndbox, "ymax").text = str(y2)

    # 保存图像
    cv2.imwrite(output_path, image)

    # 保存 XML
    xml_save_path = os.path.splitext(output_path)[0] + ".xml"
    tree = ET.ElementTree(annotation)
    tree.write(xml_save_path, encoding="utf-8", xml_declaration=True)

    print(f"Image saved: {output_path}")
    print(f"VOC XML saved: {xml_save_path}")

def visualize_detection(image_path, detected_objects, output_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 使用 ListFields 获取所有设置的字段及其值
    fields = detected_objects.ListFields()

    tags = []
    corners = []
    accuracies = []

    # 解析字段
    for field, value in fields:
        if field.name == "tag":
            tags = value  # 假设标签是列表
        elif field.name == "corner":
            corners = value  # 假设边界框是列表
        elif field.name == "accuracy":
            accuracies = value  # 假设置信度是列表

    # 确保标签、边界框和置信度的数量一致
    if len(tags) == len(corners) == len(accuracies):
        for i in range(len(tags)):
            tag = tags[i]
            corner = corners[i]
            accuracy = accuracies[i]

            # 获取边界框坐标
            x1, y1 = corner.x1, corner.y1
            x2, y2 = corner.x2, corner.y2
            # 计算宽度和高度
            width = x2 - x1
            height = y2 - y1

            # # 过滤掉长和宽小于阈值的框
            # if width < 360 and height < 360:
            #     continue

            # 绘制边界框
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 5)

            # 构造标签文本
            # label = f"insect: {accuracy:.2f}"
            label = f"{tag}: {accuracy:.2f}"

            # 确定标签的位置
            font_scale = 2  # 字体大小
            font_thickness = 3  # 字体线宽
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            label_y = max(y1, label_size[1] + 10)

            # 绘制标签背景（绿色）
            cv2.rectangle(
                image, 
                (int(x1), int(label_y) - label_size[1] - 10),  # 背景顶部左
                (int(x1) + label_size[0], int(label_y) + 10),  # 背景右下
                (0, 255, 0), 
                cv2.FILLED
            )

            # 绘制标签（黑色字体）
            cv2.putText(
                image, 
                label, 
                (int(x1), int(label_y)), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, 
                (0, 0, 0), 
                font_thickness
            )

    # 保存图像
    cv2.imwrite(output_path, image)

def parse_args():
    """
    Parses the command line arguments for the test

    Returns:
        The arguments to be used

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        type=str,
        default='/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img0928/img11',
        # default='/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img0926/test_img_kunmingzhaobiao/img',
        help='path to the image to send'
    )
    parser.add_argument(
        '--image_name',
        type=str,
        default='WechatIMG287.jpg',
        help='image name'
    )
    return parser.parse_args()


def detect_objects(stub, image_path, image_name):
    print(f'Estimating image: ' + os.path.join(image_path, image_name))
    with open(os.path.join(image_path, image_name), 'rb') as fp:
        image_bytes = fp.read()

    return stub.detect(detect_model_pb2.Image(img_name=image_name, data=image_bytes))

def test_single_model(image_path, target):
    with grpc.insecure_channel(target, options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)]) as channel:

        stub = detect_model_pb2_grpc.DetectModelStub(channel)
        try:
            image_name_list = os.listdir(image_path)
            for image_name in image_name_list:
                detected_objects = detect_objects(stub, image_path, image_name)
                print(detected_objects)
                # 输出图像保存路径
                # os.makedirs(output_path,exist_ok=True)
                # 调用可视化函数
                # visualize_detection(os.path.join(image_path,image_name), detected_objects, os.path.join(output_path,image_name))
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')

def test_all_models():
    image_path_list = [
        '/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img_0830', # 测报灯大虫50051
        '/home/yaoteam/yaoteam/yyc/YOLOv6/test_img1210', # 测报灯小虫50055
        # '/home/yaoteam/yaoteam/yyc/xiaochongti_yolov8_server/test_img', # 测报灯小虫体50052
        # '/home/yaoteam/yaoteam/yyc/bioclip_server/test_img',# Bioclip
        # '/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img0928/img14_cropimg/稻纵卷叶螟',# Bioclip
        
    ] 
    address_list = [
        '192.168.1.222:50051', # 测报灯大虫50051
        '192.168.1.222:50055', # 测报灯小虫50055
        # '192.168.1.222:50052', # 测报灯小虫体50052
        # '192.168.1.222:50057', # Bioclip
    ]
    for image_path, target in zip(image_path_list, address_list):
        test_single_model(image_path, target)
        print('=' * 50)
    
    print('All models tested successfully!')

def test_all_models_with_timing():
    start_time = time.perf_counter()
    test_all_models()
    end_time = time.perf_counter()
    return end_time - start_time  # 返回每个线程的执行时间

def main():
    # args = parse_args()
    # image_path = args.path
    # image_name = args.image_name
    image_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/img'
    # image_name = 'InSeCt_1662015804010_1.jpg'
    target = SERVER_ADDRESS

    output_path = "/home/yaoteam/yaoteam/yyc/mmdet_dino/img_output"

    # with grpc.insecure_channel(target, options=[
    #     ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    #     ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)]) as channel:

    #     stub = detect_model_pb2_grpc.DetectModelStub(channel)
    #     try:
    #         image_name_list = os.listdir(image_path)
    #         for image_name in image_name_list:
    #             detected_objects = detect_objects(stub, image_path, image_name)
    #             print(detected_objects)
    #             # 输出图像保存路径
    #             os.makedirs(output_path,exist_ok=True)
    #             # 调用可视化函数
    #             visualize_detection_and_xml(os.path.join(image_path,image_name), detected_objects, os.path.join(output_path,image_name))
    #     except grpc.RpcError as rpc_error:
    #         print('An error has occurred:')
    #         print(f'  Error Code: {rpc_error.code()}')
    #         print(f'  Details: {rpc_error.details()}')

    num_threads = 2  # 设置线程数量，可以根据需要调整
    execution_times = []  # 用来保存每个线程的执行时间
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
            futures.append(executor.submit(test_all_models_with_timing))
        
        # 等待所有线程完成，并收集每个线程的执行时间
        for future in as_completed(futures):
            execution_times.append(future.result())  # 每个线程的执行时间
    
    # 输出所有线程的执行时间
    for idx, exec_time in enumerate(execution_times):
        print(f"线程 {idx + 1} 执行时间: {exec_time:.2f} 秒")
    
    # 输出总体耗时
    total_time = sum(execution_times)
    print(f'所有线程执行完毕，总耗时：{total_time:.2f} 秒')



if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print('\n耗时：', time.perf_counter() - start, 's')
