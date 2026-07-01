import os

# 现在有两个文件夹里面有一些重复图片，现在要以一个文件夹内的图片名作为基准，删除另一个文件夹内有同样文件名的图片，python实现


def remove_duplicates(base_folder, target_folder):
    # 获取基准文件夹中的所有文件名
    base_filenames = set(os.listdir(base_folder))

    # 获取目标文件夹中的所有文件
    target_files = os.listdir(target_folder)

    # 遍历目标文件夹中的文件
    for file in target_files:
        # 如果文件名在基准文件夹中存在，则删除目标文件夹中的文件
        if file in base_filenames:
            file_path = os.path.join(target_folder, file)
            os.remove(file_path)
            # print(f"Deleted: {file_path}")

# 示例文件夹路径
base_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images'
target_folder = '/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总_81955'

# 执行删除重复文件的函数
remove_duplicates(base_folder, target_folder)
