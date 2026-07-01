import glob
from tqdm import tqdm
import os
from datautils.xml_tools import ReadAnnotation
import cv2
import xml.etree.ElementTree as ET
xml_src = r'/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/xml_for_crop'
img_src = r'/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/img_for_crop'
dst = r'/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集_论文用图/crop_img'


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
        for x1, y1, x2, y2, cls_name in xml.get_ann():

            x1 = round(float(x1))
            y1 = round(float(y1))
            x2 = round(float(x2))
            y2 = round(float(y2)) # 这里会导致无法回溯到原图，所以先要对原标注文件都转一遍round(float)，使其变成int，已整合到此代码，解决

            # 多类别
            img = image[y1:y2 + 1, x1:x2 + 1, ...]
            target = os.path.join(dst, cls_name)
            if not os.path.exists(target):
                os.mkdir(target)
            dst_file = os.path.join(target, os.path.basename(xml_file)[:-4] + f'_{x1}_{y1}_{x2}_{y2}.jpg')
            cv2.imwrite(dst_file,img, params=[cv2.IMWRITE_JPEG_QUALITY, 100])
            

if __name__ == '__main__':
    main()