import glob
from tqdm import tqdm
import os
from datautils.xml_tools import ReadAnnotation
import cv2
import xml.etree.ElementTree as ET

xml_src = r'/home/yaoteam/yaoteam/wz/mvs-photo/xml_SBPH/'
img_src = r'/home/yaoteam/yaoteam/wz/mvs-photo/SBPH/'
dst = r'/home/yaoteam/yaoteam/wz/招标虫子小图/'
# xml_src = r'/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/xml/'
# img_src = r'/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/img/'
# dst = r'/home/yaoteam/yaoteam/yyc/random_paste_work/回溯结果准确性测试/回溯/'

# classes = (
#     下面注意不要忘记设置多类别和单类别
    # 'A3', 'AB10', 'AB11', 'AM3', 'AM5', 'AQ10', 'AQ11', 'AQ20', 'AQ30', 'AQ34', 'AQ4', 'AQ43', 'AQ44', 'AS1', 'AS4', 'B14', 'B2', 'Q10', 'Q2', 'Q6', '双斑痕叶蝉', '叶蝉科', '派罗飞虱属', '灰飞虱', '烟翅白背飞虱', '玉米花翅飞虱', '电光叶蝉',
    # '白条飞虱', '白背飞虱', '白脊飞虱1', '蓼飞虱', '褐飞虱属', '锥头叶蝉属', '长绿飞虱', '飞虱科', '黑尾叶蝉', '其他类别'
#
#
# )
# classes = ('insect')
# classes = ('B138', 'B22', 'L35', 'B8')
# classes = ('黑尾叶蝉', '飞虱科', '长绿飞虱', '褐飞虱属', '蓼飞虱', '白背飞虱', '白条飞虱', '白条飞虱', '烟翅白背飞虱', '灰飞虱', '叶蝉科', '双斑痕叶蝉', '其他类别', 'Q6', 'Q2', 'Q10', 'B2', 'B14', 'AS4', 'AS1', 'AQ44', 'AQ43',
#                    'AQ4', 'AQ34', 'AQ30', 'AQ20', 'AQ11', 'AQ10', 'AM5', 'AM3', 'AB11', 'AB10', 'A3')
# classes = ('白背飞虱')
def integerize_coordinates(xml_folder_path):
    # 遍历文件夹中的每个XML文件
    for filename in os.listdir(xml_folder_path):
        if not filename.endswith('.xml'):
            continue
        
        file_path = os.path.join(xml_folder_path, filename)
        
        # 解析XML文件
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 遍历每个object标签
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            
            # 获取并整数化坐标
            x1 = round(float(bndbox.find('xmin').text))
            y1 = round(float(bndbox.find('ymin').text))
            x2 = round(float(bndbox.find('xmax').text))
            y2 = round(float(bndbox.find('ymax').text))
            
            # 更新XML中的坐标
            bndbox.find('xmin').text = str(x1)
            bndbox.find('ymin').text = str(y1)
            bndbox.find('xmax').text = str(x2)
            bndbox.find('ymax').text = str(y2)
        
        # 保存更新后的XML文件
        tree.write(file_path)

def main():
    integerize_coordinates(xml_src) #整数化原来的标签 ！！！！！！！！！！！这对后面一一对应很重要
    xml_files = glob.glob(os.path.join(xml_src, '*.xml'))
    os.makedirs(dst, exist_ok=True)
    for xml_file in tqdm(xml_files):
        img_file = os.path.join(img_src, os.path.basename(xml_file)[:-4] + '.jpg')
        if not os.path.exists(img_file):
            img_file = os.path.join(img_src, os.path.basename(xml_file)[:-4] + '.png')
        image = cv2.imread(img_file)
        # assert image is not None, f'img is None, file is {img_file}'
        if image is None:
            print(f'warning: img is None, file is {img_file},pass')
            continue
        xml = ReadAnnotation(xml_file)
        info = {}
        cls_name_one='SBPH'
        for x1, y1, x2, y2, cls_name, score in xml.get_ann():
            print(1)
            x1 = round(float(x1))
            y1 = round(float(y1))
            x2 = round(float(x2))
            y2 = round(float(y2)) # 这里会导致无法回溯到原图，所以先要对原标注文件都转一遍round(float)，使其变成int，已整合到此代码，解决
            # info[cls_name] = f'{x1}_{y1}_{x2}_{y2}'  # 命名格式要改,用其他分隔符！！！（先用脚本搜索用过的标签）包括crop_v2.py里的都要改，先裁剪小图，使用模型分类好了，每个文件夹之后用
            
            # 多类别
            # if cls_name in classes: # 多类别分类的时候这里要取消注释
            #     img = image[y1:y2 + 1, x1:x2 + 1, ...]
            #     target = os.path.join(dst, cls_name)
            #     if not os.path.exists(target):
            #         os.mkdir(target)
            #     dst_file = os.path.join(target, os.path.basename(xml_file)[:-4] + f'score:{score}' + f'_{x1}_{y1}_{x2}_{y2}.jpg')
            #     print(os.path.basename(xml_file))
            #     cv2.imwrite(dst_file,img, params=[cv2.IMWRITE_JPEG_QUALITY, 100])
            
            # 单类别

            img = image[y1:y2 + 1, x1:x2 + 1, ...]
            target = os.path.join(dst, cls_name_one)
            if not os.path.exists(target):
                os.mkdir(target)
            dst_file = os.path.join(target, os.path.basename(xml_file)[:-4] + f'_{x1}_{y1}_{x2}_{y2}.jpg')
            print(os.path.basename(xml_file))
            cv2.imwrite(dst_file, img, params=[cv2.IMWRITE_JPEG_QUALITY, 100])



if __name__ == '__main__':
    main()