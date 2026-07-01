import numpy as np
import copy

__all__ = ['get_sliding_coordinates','get_n_crop_coordinates']

def get_sliding_coordinates(img_w, img_h, sliding_win_w, sliding_win_h, over_lapping_size=206):
    """
    获取滑动窗口裁剪图片时的裁剪坐标，左上右下
    :param img_w:
    :param img_h:
    :param sliding_win_w:
    :param sliding_win_h:
    :param over_lapping_size:
    :return: [[xmin,ymin,xmax,ymax]]
    """
    if sliding_win_h > img_h:
        sliding_win_h = img_h
    if sliding_win_w > img_w:
        sliding_win_w = img_w
    base_size = [0, 0, sliding_win_w, sliding_win_h]
    # [[3,4,5,6],]
    all_coordinate = []
    next_coor = [copy.deepcopy(base_size)]
    # 列，行
    i = 1
    col_flag = False
    row_flag = False
    while True:
        if col_flag and row_flag:
            for k in next_coor:
                if k in all_coordinate:
                    continue
                all_coordinate.append(k)
            break
        if col_flag:
            x1, y1, x2, y2 = base_size
            # base_size[0] = x1
            base_size[1] = y2 - over_lapping_size
            # base_size[2] = x2
            if y2 + (sliding_win_h - over_lapping_size) > img_h:
                base_size[3] = img_h
                base_size[1] = img_h - sliding_win_h
                row_flag = True
            else:
                base_size[3] = y2 + (sliding_win_h - over_lapping_size)
            for k in next_coor:
                all_coordinate.append(k)
            next_coor = [copy.deepcopy(base_size)]
            i = 1
            col_flag = False
        x1, y1, x2, y2 = next_coor[i - 1]
        next_x1 = x2 - over_lapping_size
        next_y1 = y1
        next_x2 = next_x1 + sliding_win_w
        next_y2 = next_y1 + sliding_win_h
        if next_y2 == img_h:
            row_flag = True
        # 水平方向是否窗口超出图像边界
        if next_x2 <= img_w:
            next_coor.append([next_x1, next_y1, next_x2, next_y2])
            i += 1

            if next_x2 == img_w:
                col_flag = True
        else:
            next_x2 = img_w
            next_x1 = next_x2 - sliding_win_w

            next_coor.append([next_x1, next_y1, next_x2, next_y2])
            i += 1

            col_flag = True
    return all_coordinate

def get_n_crop_coordinates(img_w: int,
                           img_h: int,
                           n: int):
    """
    对一张图片进行裁剪分块
    :param
    :return:[[xmin,ymin,xmax,ymax],]
    """
    # img = Image.open(img_path)
    width, height = img_w, img_h
    # 每一小块图的宽，高
    patch_w = width // n
    patch_h = height // n
    # 图片裁剪功能
    # 先行后列，i是行，j是列,(i,j)表示当前小块坐标
    posi = []
    for i in range(n):
        for j in range(n):
            # 有的小图没有标注，不需要保存
            box = (j * patch_w, i * patch_h, (j + 1) * patch_w, (i + 1) * patch_h)
            posi.append(box)
    return posi



if __name__ == '__main__':
    # coor = get_sliding_coordinates(150, 150, 150, 150, 0)
    # step_w = 150
    # step_h = 150
    # for x1, y1, x2, y2 in coor:
    #     if x2 - x1 > step_w or y2 - y1 > step_h:
    #         print(x2 - x1)
    #         print(y2 - y1)
    # print(len(coor))
    # print(coor)
    import timeit
    print(timeit.timeit('get_n_crop_coordinates(11,8,2)','from  __main__ import get_n_crop_coordinates',number=1000))
    print(timeit.timeit('crop_img(11,8,2)','from  __main__ import crop_img',number=1000))
    # print(crop_img(11,8,2))
