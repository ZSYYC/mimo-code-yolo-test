import os

def count_files_in_subfolders(root_folder):
    for subdir, _, files in os.walk(root_folder):
        if subdir == root_folder:
            continue
        num_files = len(files)
        print(f"Folder '{os.path.basename(subdir)}' contains {num_files} files.")

# 示例用法
root_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/crop_img_2000_checked_putong_swinB_classfied0807_agglomerative_epoch_219_cluster_output'
count_files_in_subfolders(root_folder)
