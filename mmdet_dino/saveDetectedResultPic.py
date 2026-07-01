from datetime import datetime
import os.path
import detect_model_pb2
import pymysql
import sys
import cv2
from PIL import Image, ImageFont, ImageDraw
import grpc
import io
from db_client import DatabaseClient
import getpass
import subprocess

db_config = {
    'host': '121.199.54.94',
    'port': 3306,
    'user': 'root',
    'password': 'ZsTu@Ecs@2025',
    'database': 'ry-vue-zdnzw',
    'charset': 'utf8'
}
base_path = '/home/yaoteam/yaoteam/chongti_images/'

def save_detected_result(label_list, box_list, img_name, img_path):

    classes = []
    db_client = DatabaseClient(db_config)
    # 创建当天图片文件夹
    today_str = datetime.today().strftime('%Y-%m-%d')
    folder_path_date = os.path.join(base_path, today_str)
    os.makedirs(folder_path_date, exist_ok=True)

    # 创建类别文件夹
    # for label in label_list:
    #     folder_path_class = os.path.join(folder_path_date, label)
    #     os.makedirs(folder_path_class, exist_ok=True)
    #     if label not in classes:
    #         classes.append(label)

    result = db_client.query_by_name(img_name)
    # print(result)
    row = result[0]
    device_name = row[0]
    img_real_name = row[1]
    photo_time = row[2]
    # print(device_name, img_real_name, photo_time)

    image = cv2.imread(img_path)
    corners = []
    for box in box_list:
        obj_corner = detect_model_pb2.Corner(x1=box[0], y1=box[1], x2=box[2], y2=box[3])
        corners.append(obj_corner)

    for label, corner in zip(label_list, corners):
        # print(corner)
        x1 = round(float(corner.x1))
        y1 = round(float(corner.y1))
        x2 = round(float(corner.x2))
        y2 = round(float(corner.y2))
        img = image[y1:y2 + 1, x1:x2 + 1, ...]
        #dst_file = os.path.join(folder_path_date, label, f'{device_name}+{img_real_name}+{label}+{timestamp_str}+x1:{x1}+y1:{y1}+x2:{x2}+y2:{y2}.jpg')
        dst_file = os.path.join(folder_path_date,
                                f'{label}+{device_name}+{img_real_name}+{photo_time}+{x1}+{y1}+{x2}+{y2}.jpg')
        cv2.imwrite(dst_file, img, params=[cv2.IMWRITE_JPEG_QUALITY, 100])

    db_client.close()