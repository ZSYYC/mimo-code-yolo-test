import argparse
import os
import grpc

import detect_model_pb2
import detect_model_pb2_grpc
from tqdm import tqdm
import time
import csv
# server address
# SERVER_ADDRESS = "192.168.1.216:9222"
SERVER_ADDRESS = "192.168.1.222:50051"
# max message length: 256MB
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024

import cv2
# 定义字典存储第二列和第四列的对应关系
result_dict = {}

# 读取CSV文件
with open('/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过第一行（表头）

    # 从第二行开始读取每一行
    for row in reader:
        key = row[3]  # 第二列
        value = row[1]  # 第四列
        result_dict[key] = value  # 将第二列作为键，第四列作为值

# 打印生成的字典
print(result_dict)

class CategoryCounter:
    def __init__(self):
        self.categories = {}

    def add(self, category):
        if category in self.categories:
            self.categories[category] += 1
        else:
            self.categories[category] = 1

    def get_count(self, category):
        return self.categories.get(category, 0)

    def get_all_counts(self):
        return self.categories

def count_detection(detected_objects):

    categories_to_add = []
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
            try:
                categories_to_add.append(result_dict[tags[i]])
            except KeyError:
                categories_to_add.append(tags[i])  # 当出现KeyError时，添加tags[i]
    return categories_to_add



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

            # 绘制边界框
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # 构造标签文本
            label = f"{tag}: {accuracy:.2f}"

            # 确定标签的位置
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            label_y = max(y1, label_size[1])

            # 绘制标签背景
            cv2.rectangle(image, (int(x1), int(label_y) - label_size[1]), (int(x1) + label_size[0], int(label_y) + 10), (0, 255, 0), cv2.FILLED)

            # 绘制标签
            cv2.putText(image, label, (int(x1), int(label_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

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
        default='/home/yaoteam/yaoteam/yyc/mmdet_dino/216gkTraplight_image',
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


def main():
    args = parse_args()
    image_path = args.path
    image_name = args.image_name
    # image_path = '/home/yaoteam/fzl/xingyou-rpc'
    # image_name = 'InSeCt_1662015804010_1.jpg'
    target = SERVER_ADDRESS
    counter = CategoryCounter()
    # output_path = "/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img0928/out7"

    with grpc.insecure_channel(target, options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)]) as channel:

        stub = detect_model_pb2_grpc.DetectModelStub(channel)
        try:
            image_name_list = os.listdir(image_path)
            for image_name in tqdm(image_name_list, desc="Processing images"):
                time.sleep(0.1)
                detected_objects = detect_objects(stub, image_path, image_name)
                # print(detected_objects)
                categories_to_add = count_detection(detected_objects)
                for category in categories_to_add:
                    counter.add(category)
                # 输出图像保存路径
                # os.makedirs(output_path,exist_ok=True)
                # # 调用可视化函数
                # visualize_detection(os.path.join(image_path,image_name), detected_objects, os.path.join(output_path,image_name))
            
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')
    # 输出每个类别的数量
    for category, count in counter.get_all_counts().items():
        print(f"{category}: {count}")


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print('\n耗时：', time.perf_counter() - start, 's')
