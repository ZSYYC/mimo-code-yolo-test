# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
# from xml import xml as ET
from PIL import Image
def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        objects.append(obj_struct)
    return objects
def read_image(image_path, filename):
    im = Image.open(image_path + filename)
    W = im.size[0]
    H = im.size[1]
    area    = W * H
    im_info = [W, H, area]
    return im_info


if __name__ == '__main__':
    xml_path ='/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/xml/'
    # xml_path =r'/home/SATA2/lhl/bbfshfsyechan-mix/Annotations_utf8/'
    filenamess = os.listdir(xml_path)
    filenames = []
    for name in filenamess:
        name = name.replace('.xml', '')
        filenames.append(name)
    recs = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')
    for name in filenames:
        for object in recs[name]:
            if object['name']=="l3"or object['name']=="l4":
                print(name)
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
            if object['name'] not in classnames:
                classnames.append(object['name'])
    for name in classnames:
        print('{}:{}个'.format(name, num_objs[name]))
    print('信息统计算完毕。')




