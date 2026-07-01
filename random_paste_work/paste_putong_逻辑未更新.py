import glob
import os
import random
import shutil

import cv2
import torch
from datautils.xml_tools import ReadAnnotation, write2xml
from torchvision.ops import box_iou
from tqdm import tqdm

src_img = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗/JPEGImages' #代扩增目标图片
src_xml = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗/Annotations'
img_path = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗/crop_img'  # 小图路径

target_root = '/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗/VOC_paste' #输出目录
target_img = os.path.join(target_root, 'img')
target_xml = os.path.join(target_root, 'xml')

def random_img(img_files, cls, p=0.5):
    # 每个类别有0.5的概率随机选中的各自类别的一个图片
    if random.random() < p:
        return random.choice(img_files[cls])
    return None

def check_nums(cur_nums):
    return sum(cur_nums) >= sum(nums)

def get_bboxes(xml_file):
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

def get_target_files(prefix_path):
    target_img = {}
    for cls in clses:
        files = glob.glob(os.path.join(prefix_path,cls,'*.jpg'))     #读取的图片格式 ！！！！！！！
        target_img[cls] = files
    return target_img

def anchor_generator(ws, hs, img_w, img_h, stride_w, stride_h, dtype=torch.int16):
    """
    根据要粘贴到图片上的小目标大小，在原图上生成anchor,且anchors在图片范围内
    @param ws: 小目标图片宽
    @param hs: 小目标图片高
    @param img_w: 原图宽
    @param img_h: 原图高
    @param stride_w: 水平步长
    @param stride_h:
    @param dtype:
    @return: torch.tensor, shape=(n,4)
    """
    x_center,y_center = 0, 0
    base_anchors = [
        x_center - 0.5 * ws, y_center - 0.5 * hs, x_center + 0.5 * ws,
        y_center + 0.5 * hs
    ]
    base_anchors = torch.tensor(base_anchors).to(dtype)
    base_anchors = base_anchors[None,:]
    shift_x = torch.arange(0, img_w, step=stride_w).to(dtype)
    shift_y = torch.arange(0, img_h, step=stride_h).to(dtype)
    xx = shift_x.repeat(shift_y.shape[0])
    yy = shift_y.view(-1, 1).repeat(1, shift_x.shape[0]).view(-1)
    shifts = torch.stack([xx, yy, xx, yy], dim=-1)
    all_anchors = base_anchors[None, :, :] + shifts[:, None, :]
    all_anchors = all_anchors.view(-1, 4)
    valid_indes = (all_anchors[:,0] > 0) & (all_anchors[:, 1] > 0) \
                  & (all_anchors[:,2] < img_w) & (all_anchors[:,3] < img_h)
    return all_anchors[valid_indes]

def single_cls_location(gt, anchors, iou_thr=0.25):
    overlaps = box_iou(gt, anchors)
    max_overlaps, argmax_overlaps = overlaps.max(dim=0)
    assigned_anchor_inds = max_overlaps <= iou_thr
    assigned_anchors = anchors[assigned_anchor_inds]
    # TODO 会出现原图目标太多，没有放小图的位置
    if assigned_anchors.numel() > 0:
        row_index = torch.randint(0, assigned_anchors.size(0), (1, ))
        return assigned_anchors[row_index, :]
    else:
        return None

def random_albu(img, p=0.5):
    if random.random() < p:
        # 旋转90度
        img = cv2.transpose(img)
        img = cv2.flip(img, 1)
        return img
    if random.random() < p:
        img = cv2.flip(img, -1)
        return img
    if random.random() < p:
        img = cv2.transpose(img)
        img = cv2.flip(img, 0)
        return img
    if random.random() < p:
        img = cv2.flip(img, 1)
        return img
    if random.random() < p:
        img = cv2.flip(img, 0)
        return img
    return img

def main():
    assert len(nums) == len(clses)
    xml_files = glob.glob(os.path.join(src_xml, '*.xml'))
    assert len(xml_files) > 0
    cur_nums = [0 for _ in range(len(nums))]
    is_enough = False
    # 获取需要增加数量的类别的所有图片路径
    target_img_files = get_target_files(img_path)
    # print(target_img_files)

    is_first = True
    while not is_enough:
        if not is_first:
            xml_files = glob.glob(os.path.join(target_xml, '*.xml'))
        for xml_file in tqdm(xml_files):
            if not is_first:
                img_file = os.path.join(target_img, os.path.basename(xml_file)[:-4] + '.jpg')
                if not os.path.exists(img_file):
                    img_file = os.path.join(target_img, os.path.basename(xml_file)[:-4] + '.png')
            else:
                img_file = os.path.join(src_img, os.path.basename(xml_file)[:-4] + '.jpg')
                if not os.path.exists(img_file):
                    img_file = os.path.join(src_img, os.path.basename(xml_file)[:-4] + '.png')

            image = cv2.imread(img_file)
            w, h = image.shape[1], image.shape[0]
            # 获取gt
            bboxes_cls = get_bboxes(xml_file)
            bboxes = [v[:-1] for v in bboxes_cls]
            bboxes = torch.tensor(bboxes)
            for idx, cls in enumerate(clses):
                # if check_nums(cur_nums):
                #     return
                if cur_nums[idx] == nums[idx]:
                    continue
                target_file = random_img(target_img_files, cls)
                if target_file is not None:
                    assert os.path.exists(target_file)
                    small_img = cv2.imread(target_file)
                    small_img = random_albu(small_img)
                    small_img_w, small_img_h = small_img.shape[1], small_img.shape[0]
                    anchors = anchor_generator(small_img_w, small_img_h, w, h, small_img_w // 2, small_img_h // 2)
                    
                    # 检查 bboxes 是否为空
                    if bboxes.numel() > 0:
                        location = single_cls_location(bboxes, anchors)
                    else:
                        # bboxes 为空时，随机选择一个位置
                        if anchors.numel() > 0:
                            row_index = torch.randint(0, anchors.size(0), (1, ))
                            location = anchors[row_index, :]
                        else:
                            location = None      
                            
                    if location is None:
                        continue
                    bboxes = torch.cat((bboxes, location), dim=0)
                    cur_nums[idx] += 1
                    small_height, small_width, _ = small_img.shape
                    x1, y1, x2, y2 = location.squeeze().tolist()
                    bboxes_cls.append([x1,y1,x1+small_width,y1+small_height,cls])
                    # try:
                    image[y1:y1+small_height,x1:x1+small_width] = small_img
                    # except Exception as e:
                    #     print()
            if not check_nums(cur_nums):
                cv2.imwrite(os.path.join(target_img,os.path.basename(img_file)), image, params=[cv2.IMWRITE_JPEG_QUALITY, 100])
                write2xml(w,h, bboxes_cls, os.path.join(target_xml, os.path.basename(xml_file)))
            elif is_first:
                shutil.copyfile(img_file, os.path.join(target_img, os.path.basename(img_file)))
                shutil.copyfile(xml_file, os.path.join(target_xml, os.path.basename(xml_file)))
        is_first = False
        is_enough = check_nums(cur_nums)


if __name__ == '__main__':
    if not os.path.exists(target_img):
        os.makedirs(target_img)
    if not os.path.exists(target_xml):
        os.makedirs(target_xml)
    # 需要添加的类别与添加数量
    clses = ['bbfs','hui']
    # clses = ['y1']
    nums = [600,2000]
    # nums = [10]
    main()