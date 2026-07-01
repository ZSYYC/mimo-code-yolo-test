#!/bin/bash

# 源文件夹路径
dir="/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总"

# 查找并处理所有软链接
find "$dir" -type l | while read link; do
  # 获取软链接指向的源文件
  src_file=$(readlink -f "$link")
  
  # 获取软链接的目标路径
  dest_file="$link"
  
  # 复制源文件到目标路径，覆盖软链接
  cp "$src_file" "$dest_file"
done
