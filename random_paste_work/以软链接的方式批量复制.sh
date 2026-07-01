#!/bin/bash

# 源文件夹和目标文件夹
src_dir="/home/yaoteam/yaoteam/yyc/random_paste_work/test/img"
dest_dir="/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总"
# src_dir="/home/yaoteam/yaoteam/yyc/random_paste_work/虫情测报灯罗浩伦数据集/VOC/JPEGImages"
# dest_dir="/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总"

# 创建目标文件夹（如果不存在）
mkdir -p "$dest_dir"

# 遍历源文件夹中的所有图片文件并创建软链接
for file in "$src_dir"/*.{jpg,jpeg,png,bmp}; do
  # 检查文件是否存在（处理无匹配文件的情况）
  if [ -e "$file" ]; then
    ln -s "$file" "$dest_dir/$(basename "$file")"
  fi
done
