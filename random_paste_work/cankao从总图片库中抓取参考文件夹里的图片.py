import os
import shutil
# 给定两个图片文件夹，A和B。B文件夹里的图片是A的子集，现在要从A中再拷贝一份B出来，保存到C目录
def copy_images(A_dir, B_dir, C_dir):
    # 确保C目录存在
    if not os.path.exists(C_dir):
        os.makedirs(C_dir)

    # 获取B目录中的所有图片文件
    B_images = set(os.listdir(B_dir))

    # 遍历A目录中的文件
    for image_name in os.listdir(A_dir):
        if image_name in B_images:
            # 构建源文件路径和目标文件路径
            src_path = os.path.join(A_dir, image_name)
            dest_path = os.path.join(C_dir, image_name)

            # 复制文件到C目录
            shutil.copy(src_path, dest_path)
            print(f"Copied: {image_name}")

# 示例使用
A_dir = "/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/网站/其他几个测报灯图片" # 图片库
B_dir = "/home/yaoteam/yaoteam/yyc/mmdet_dino/20241210_det_xiaochong_images" # 参考
C_dir = "/home/yaoteam/yaoteam/yyc/mmdet_dino/20241210_det_xiaochong_images_ori" # 图片库中参考的拷贝

copy_images(A_dir, B_dir, C_dir)
