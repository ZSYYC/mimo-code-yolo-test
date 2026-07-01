import glob
import os
import random

import albumentations as A
import cv2
from datautils.xml_tools import ReadAnnotation
from torchvision.ops import box_iou
from datautils.coordinates_tools import *
import threading
__all__ = ['crop_pad', 'scale_img', 'horizontal_flip_img','bbox2bboxes','crop', 'safe_rotate', 'rotate', 'rotate90']

'''
    主要封装了albumentations中的图像增强方法
'''
# https://albumentations.ai/docs/getting_started/bounding_boxes_augmentation/

def rotate90(image, bboxes):
    """
    顺时针旋转90，用于exif信息忘记清楚就进行了标记的图片，使用PIL读取的图片宽和高与实际图片宽高对调了
    @param image:
    @param bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    @return:
    """
    img_h, img_w, _= image.shape
    image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
    rotated_bboxes = []
    for xmin, ymin, xmax, ymax, cls_name in bboxes:
        rotated_bboxes.append([img_h - ymax, xmin, img_h - ymin, xmax, cls_name])

    return image, rotated_bboxes

def safe_rotate(image, bboxes, limit, p=1):
    transform = A.Compose(
        [
            A.SafeRotate(limit=limit,p=p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.99)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes

def rotate(image, bboxes, limit, p=1):
    transform = A.Compose(
        [
            A.Rotate(limit=limit,p=p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.7)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes
def crop_pad(image, bboxes, px=None, percent=None, keep_size=True, pad_mode=cv2.BORDER_REFLECT101, p: float = 1.0):
    """
    裁剪填充，px和percent只能用一个
    :param image:
    :param bboxes:
    :param px: [top, right, bottom, left],int
    :param percent:[top, right, bottom, left],float
    :param keep_size: 保持原图尺寸
    :param pad_mode: opencv中的填充模式
    :param p: 是否执行操作的概率
    :return: (增强后的img, 增强后的bbox)
    """
    transform = A.Compose(
        [
            A.CropAndPad(px=px, percent=percent, pad_mode=pad_mode, keep_size=keep_size, p=p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.7)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes



def crop(image, bboxes, xmin, ymin, xmax, ymax):
    """

    :param image:
    :param bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
    :return: 返回的bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    """
    transform = A.Compose(
        [
            A.Crop(xmin, ymin, xmax, ymax)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.99)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes

def crop_bboxes(img_w,img_h, bboxes, xmin, ymin, xmax, ymax):
    """

    :param image:
    :param bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
    :return: 返回的bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    """




def scale_img_by_ratio(image, w, h, bboxes, ratio: float = 1.5, p: float = 1.0):
    """
    图片放大
    :param image:
    :param w: 原图像w
    :param h: 原图像h
    :param bboxes:bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    :param ratio: 放缩倍数
    :param p:
    :return:
    """
    transform = A.Compose(
        [
            A.Resize(int(float(h) * ratio), int(float(w) * ratio), p=p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.7)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes

def scale_img(image, w, h, bboxes,  p: float = 1.0):
    """
    图片放大
    :param image:
    :param w: resize后的w
    :param h: resize后的h
    :param bboxes:bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    :param ratio: 放缩倍数
    :param p:
    :return:
    """
    transform = A.Compose(
        [
            A.Resize(h, w, p=p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.7)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes

def smallest_maxsize_img(img,bboxes ,max_size, p=1.0):
    transform = A.Compose(
        [
            A.SmallestMaxSize(max_size, p=p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.7)
    )
    transformed = transform(image=img, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes
def horizontal_flip(image, bboxes, p=1):
    """

    :param image:
    :param bboxes: [[x1, y1, x2, y2, cls_name],[]]
    :param p:
    :return: bboxes:[[xmin, ymin, xmax, ymax, cls_name]]
    """
    transform = A.Compose(
        [
            A.HorizontalFlip(p)
        ],
        bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.7)
    )
    transformed = transform(image=image, bboxes=bboxes)
    augmented_img = transformed['image']
    augmented_bboxes = transformed['bboxes']
    return augmented_img, augmented_bboxes

def horizontal_flip_img(xml_file,img_file):
    """
    对图片水平反转，并修改xml
    :param xml_file:
    :param img_file:
    :return:
    """
    xml = ReadAnnotation(xml_file)
    image, bboxes = _bbox2bboxes(xml_file,img_file)
    augmented_img, augmented_bboxes = horizontal_flip(image, bboxes)
    return xml.width,xml.height,augmented_img, augmented_bboxes

def bbox2bboxes(xml_file):
    """
    将xml文件所有box组合成[[xmin,ymin,xmax,ymax,cls_name]]
    :param xml_file:
    :param img_file:
    :return:
    """
    xml = ReadAnnotation(xml_file)
    bboxes = []
    for x1, y1, x2, y2, cls_name in xml.get_ann():
        bbox = []
        bbox.append(int(x1))
        bbox.append(int(y1))
        bbox.append(int(x2))
        bbox.append(int(y2))
        bbox.append(cls_name)
        bboxes.append(bbox)

    return bboxes

def _bbox2bboxes(xml_file,img_file):
    """
    将xml文件所有box组合成[[xmin,ymin,xmax,ymax,cls_name]]
    :param xml_file:
    :param img_file:
    :return:
    """
    xml = ReadAnnotation(xml_file)
    bboxes = []
    for x1, y1, x2, y2, cls_name in xml.get_ann():
        bbox = []
        bbox.append(int(x1))
        bbox.append(int(y1))
        bbox.append(int(x2))
        bbox.append(int(y2))
        bbox.append(cls_name)
        bboxes.append(bbox)
    image = cv2.imread(img_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, bboxes

def random_paste(img_file, small_img_path_prefix, cls_nums):
    small_files = glob.glob(os.path.join(small_img_path_prefix, '*.jpg'))
    assert len(small_files) > 0
    for _ in range(10):

        target_file = random.sample(small_files,1)
        print(target_file)

if __name__ == '__main__':
    img_path = r'H:\shenghaiyuan\data\white_plate\train\all_train_data\croped_img\B-BPH-adult'
    cls_nums = {'B-BPH-adult':20}
    random_paste(None, img_path, cls_nums)
