import os
import re

path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/水稻所拍摄'
files = os.listdir(path)
i = 0
for file in files:
    pattern = ''
    oldname = os.path.join(path,files[i])
    newname = os.path.join(path,files[i].replace(pattern,''))
    os.rename(oldname,newname)
    i += 1