import argparse
import os
import grpc
import detect_model_pb2
import detect_model_pb2_grpc
import cv2
import time
import jieba
import mysql.connector
import csv
jieba.load_userdict('user.txt')
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
connection = mysql.connector.connect(
        host='121.199.54.94',  # 数据库主机
        database='ry-vue-zdnzw',  # 数据库名称
        user='root',  # 数据库用户名
        password='zStUiNsEct@2022'  # 数据库密码
    )
cursor = connection.cursor()
# dataset1= '/home/star/yyc/datasets/何工纠正一二类害虫数据集/train0806'
cursor.execute("SELECT * FROM ser_insect_permi")
insect_list = cursor.fetchall()
insects_name = []
for insect in insect_list:
    insects_name.append(insect[1])



# 定义字典存储第二列和第四列的对应关系
result_dict = {}

# 读取CSV文件
with open('/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过第一行（表头）

    # 从第二行开始读取每一行
    for row in reader:
        key = row[1]  # 第二列
        value = row[3]  # 第四列
        result_dict[key] = value  # 将第二列作为键，第四列作为值

# 打印生成的字典
# print(result_dict)
# 键值反转
reversed_dict = {value: key for key, value in result_dict.items()}
def get_name(label):
    return reversed_dict.get(label, label)

def get_label(name):
    return result_dict.get(name, name)

# server address
SERVER_ADDRESS = "192.168.1.222:50051"
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024


def crop_and_save_object(image_path, detected_objects, output_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 使用 ListFields 获取所有设置的字段及其值
    fields = detected_objects.ListFields()

    tags = []
    corners = []

    # 解析字段
    for field, value in fields:
        if field.name == "tag":
            tags = value  # 假设标签是列表
        elif field.name == "corner":
            corners = value  # 假设边界框是列表

    # 确保标签和边界框的数量一致
    if len(tags) == len(corners):
        for i in range(len(tags)):
            tag = tags[i]
            tag = get_name(tag) # 记录中文标签
            corner = corners[i]

            # 获取边界框坐标
            x1, y1 = corner.x1, corner.y1
            x2, y2 = corner.x2, corner.y2

            # 裁剪图像
            cropped_image = image[int(y1):int(y2), int(x1):int(x2)]

            # 创建类别文件夹
            category_dir = os.path.join(output_path, tag)
            os.makedirs(category_dir, exist_ok=True)

            # 构造裁剪图像保存路径
            cropped_image_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_{int(y1)}_{int(y2)}_{int(x1)}_{int(x2)}.jpg"
            cropped_image_path = os.path.join(category_dir, cropped_image_name)

            # 保存裁剪后的图像
            cv2.imwrite(cropped_image_path, cropped_image)
            print(f"Saved cropped image: {cropped_image_path}")


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
        default='/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img0928/img14',
        help='path to the image to send'
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
    target = SERVER_ADDRESS

    output_path = "/home/yaoteam/yaoteam/yyc/mmdet_dino/test_img0928/img14_cropimg"

    with grpc.insecure_channel(target, options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)]) as channel:

        stub = detect_model_pb2_grpc.DetectModelStub(channel)
        try:
            image_name_list = os.listdir(image_path)
            for image_name in image_name_list:
                detected_objects = detect_objects(stub, image_path, image_name)
                # print(detected_objects)
                # 调用裁剪保存函数
                crop_and_save_object(os.path.join(image_path, image_name), detected_objects, output_path)
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print('\n耗时：', time.perf_counter() - start, 's')
