import os
import shutil

def copy_matching_files(dir_a, dir_b, dir_c):
    # 确保目标文件夹C存在，不存在则创建
    os.makedirs(dir_c, exist_ok=True)

    # 获取目录B中的所有文件名
    files_in_b = set(os.listdir(dir_b))

    # 遍历目录A中的文件
    for file_name in os.listdir(dir_a):
        # 如果A中的文件在B中也存在（同名）
        if file_name in files_in_b:
            # 构建文件的完整路径
            src_file = os.path.join(dir_a, file_name)
            dest_file = os.path.join(dir_c, file_name)
            
            # 复制文件到C目录
            shutil.copy(src_file, dest_file)
            print(f"复制文件: {file_name} 到 {dir_c}")

# 示例用法
dir_a = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images_for_small_targets_xml'  # 替换为目录A的路径
dir_b = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/论文数据集展示用500/xml'  # 替换为目录B的路径
dir_c = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/论文数据集展示用500/小虫xml'  # 替换为目录C的路径

copy_matching_files(dir_a, dir_b, dir_c)
