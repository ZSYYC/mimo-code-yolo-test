import requests
import os
import time
import json
import random
import argparse
import datetime
import numpy as np
import xml.etree.ElementTree as ET
import glob  # 导入 glob 模块
import cv2
import time
import jieba
import mysql.connector
import csv
from tqdm import tqdm  # 进度条库
import numpy as np
from PIL import Image, ImageDraw, ImageFont  # 用于支持中文字体

url = 'http://192.168.1.222:9247/upload'
# image_path = '/home/yaoteam/yaoteam/yyc/Swin-Transformer/data/crop_putong_9/val/dz/20240201162456581_1077_2288_1313_2542.jpg'

# 加载自定义词典
jieba.load_userdict('/home/yaoteam/yaoteam/yyc/mmdet_dino/user.txt')

# 定义标签类别
category_names = [
    "水螟科", "灯蛾科", "卷叶蛾科", "苔蛾科", "龙虱科", "天牛科", "金龟科", "隐翅虫科", "叩甲科", "虎甲科",
    "叶蝉科", "胡蜂科", "螽斯科", "鳃金龟亚科", "蓑蛾科", "蝽科", "蝉科", "天蛾科", "卷蛾科", "夜蛾科",
    "螟蛾科", "毒蛾科", "舟蛾科", "泥蜂科", "叶甲科", "葬甲科", "象甲科", "蠼螋科", "萤科", "大蚊科",
    "眼蕈蚊科", "蝇科", "飞虱科", "巢蛾科", "朽木甲科", "长蝽科", "姬缘蝽科", "草螟科", "瓢虫科", "蚊科",
    "尺蛾科", "步甲科", "锥飞虱亚科", "粒脉蜡蝉科", "刺蛾科", "姬蜂科", "瘿蜂科", "犀金龟科",
    "牙甲科", "蜡蝉科", "凤蝶科", "吉丁科", "蛛甲科", "沼梭甲科", "溪泥甲科", "擎爪泥甲科", "毛泥甲科",
    "长泥甲科", "阎甲科", "蚁形甲科", "拟天牛科", "拟步甲科", "三栉牛科", "芫菁科", "幽甲科", "暗天牛科",
    "郭公虫科", "细花萤科", "粪金龟科", "锹甲科", "黑蜣科", "皮金龟科", "六甲科", "拟球甲科", "邻坚甲科",
    "小花甲科", "大蕈甲科", "露尾甲科", "隐颚扁甲科", "锯谷盗科", "花萤科", "红萤科", "球蕈甲科", "长角象科",
    "卷象科", "三锥象科", "象甲科", "牙甲科", "硕蠊科", "姬蠊科", "蜚蠊科", "木蚁科", "鼻白蚁科", "木白蚁科",
    "白蚁科", "鳖蠊科", "肥螋科", "垫跗螋科", "球螋科", "丝尾螋科", "蝗科", "脊蜢科", "锥头蝗科", "蚱科",
    "泽蚤蝼科", "蚤蝼科", "鳞蟋科", "树蟋科", "蛛蟋科", "蛉蟋科", "蚁蟋科", "驼螽科", "蟋螽科", "驼螽科",
    "蟋螽科", "沙螽科", "蜜蜂科", "方头泥蜂科", "分舌蜂科", "隧蜂科", "小蜂科", "跳小蜂科", "金小蜂科",
    "长尾小蜂科", "蚁科", "茧蜂科", "蛛蜂科", "蚁蜂科", "三节叶蜂科", "锤角叶蜂科", "叶蜂科", "土蜂科",
    "齿蛉科", "草蛉科", "褐蛉科", "螳蛉科", "蝶角蛉科", "蚁蛉科", "蟋蟀科", "色蟌科", "溪蟌科", "扇蟌科",
    "蟌科", "扁蟌科", "蜓科", "春蜓科", "蜻科", "大伪蜻科", "扁蜉科", "食虫虻科", "蜂虹科", "长足虻科",
    "蜂虻科", "果蝇科", "水蝇科", "缟蝇科", "花蝇科", "粪蝇科", "指角蝇科", "圆目蝇科", "丽蝇科", "鼻蝇科",
    "麻蝇科", "寄蝇科", "潜蝇科", "刺股蝇科", "扁足蝇科", "沼蝇总科", "鼓翃蝇科", "水虻科", "食蚜蝇科",
    "实蝇科", "广囗蝇科", "菌蚊科", "蛾蠓科", "长角蛾科", "蚕蛾科", "箩纹蛾科", "桦蛾科", "大蚕蛾科",
    "钩蛾科", "凤蛾科", "宽蛾科", "麦蛾科", "织蛾科", "绢蛾科", "尺蛾科", "燕蛾科", "细蛾科", "枯叶蛾科",
    "目夜蛾科", "尾夜蛾科", "瘤蛾科", "羽蛾科", "螟蛾科", "网蛾科", "谷蛾科", "雕蛾科", "斑蛾科", "弄蝶科",
    "灰蝶科", "蛱蝶科", "粉蝶科", "蚬蝶科", "长角石蛾科", "沼石蛾科", "蚜科", "蚧科", "胭蚧科", "盾蚧科",
    "粉蚧科", "松干蚧科", "绵蚧科", "旌蚧科", "尖胸沬蝉科", "沬蝉科", "长盾沫蝉科", "巢沫蝉科", "袖蜡蝉科",
    "象蜡蝉科", "蛾蜡蝉科", "瓢蜡蝉科", "璐蜡蝉科", "广翅蜡蝉科", "扁蜡蝉科", "角蝉科", "木虱科", "姬蝽科",
    "盲蝽科", "扁蝽科", "蛛缘蝽科", "缘蝽科", "跷蝽科", "束蝽科", "大眼长蝽科", "莎长蝽科", "室翅长蝽科",
    "地长蝽科", "同蝽科", "球蝽科", "土蝽科", "兜蝽科", "龟蝽科", "盾蝽科", "荔蝽科", "大红蝽科", "红蝽科",
    "黾蝽科", "宽肩蝽科", "水蝽科", "蟾蝽科", "划蝽科", "负子蝽科", "蝎蝽科", "蚤蝽科", "仰蝽科", "蜍蝽科",
    "猎蝽科", "网蝽科", "管蓟马科", "蓟马科", "瓢甲类", "寄生蜂类", "隐翅甲类", "松毛虫属", "黄毒蛾属",
    "白毒蛾属", "美苔蛾属", "钻夜蛾属", "褐飞虱属", "梳爪叩甲属", "园蛛属",
    "派罗飞虱属", "锥头叶蝉属", "粘夜蛾属", "流夜蛾属", "艳夜蛾属", "线天蛾属", "点夜蛾属",
    "华小卷蛾属", "垫甲属", "线刺蛾属", "花翅飞虱属", "稻绿缘蝽属", "星雪灯蛾属", "金星尺蛾属",
    "纶夜蛾属", "栉附夜蛾属", "剑纹夜蛾属", "嘴壶夜蛾属", "婪步甲属"
]

# 数据库连接
connection = mysql.connector.connect(
    host='121.199.54.94',
    database='ry-vue-zdnzw',
    user='root',
    password='zStUiNsEct@2022'
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM ser_insect_permi")
insect_list = cursor.fetchall()
insects_name = [insect[1] for insect in insect_list]

# CSV文件读取
result_dict = {}
with open('/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi.csv', mode='r', newline='') as file:
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


def get_insect_label(image_path):
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        cls_results = response.json()
        return cls_results['top5_predictions'][0]['class_index']
    else:
        print('Error:', response.status_code, response.text)


def process_voc_dataset(folder_path):


    # 构造目标文件夹路径
    target_folder = os.path.join(folder_path, 'UpdatedAnnotations')

    # 检查目标文件夹是否存在，如果不存在则创建它
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for xml_file in glob.glob(os.path.join(folder_path, 'xml', '*.xml')):
        # print(f'正在处理第{img_count}张图片-------->>')
        # img_count = img_count + 1
        tree = ET.parse(xml_file)
        root = tree.getroot()
        jpg_file = os.path.join(folder_path, 'img', root.find('filename').text)

        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            xmin = round(float(bndbox.find('xmin').text))
            ymin = round(float(bndbox.find('ymin').text))
            xmax = round(float(bndbox.find('xmax').text))
            ymax = round(float(bndbox.find('ymax').text))

            # 使用cv2读取和裁剪图像
            img = cv2.imread(jpg_file)
            cropped_img = img[ymin:ymax + 1, xmin:xmax + 1, ...]
            dst_file = os.path.join(folder_path,f'{xmin}_{ymin}_{xmax}_{ymax}.jpg') #这里很鸡肋
            cv2.imwrite(dst_file,cropped_img, params=[cv2.IMWRITE_JPEG_QUALITY, 100])
            new_category = get_insect_label(dst_file)
            os.remove(dst_file)
            # if(new_category == 'SBPH'):
            #     sbphsum += 1
            obj.find('name').text = get_name(new_category)

        tree.write(os.path.join(target_folder, os.path.basename(xml_file))) #结果保存文件夹需要自己事先创建好否则会报错

process_voc_dataset('/home/yaoteam/yaoteam/yyc/mmdet_dino/灯诱昆虫论文泛化性实验与结果展示部分20250106/灯诱昆虫')