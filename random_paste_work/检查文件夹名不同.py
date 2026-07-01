import os

def check_diff_files(folder1, folder2):
    # 获取文件夹1和文件夹2中的所有文件名
    files_folder1 = set(os.listdir(folder1))
    files_folder2 = set(os.listdir(folder2))

    # 找到文件夹1中有而文件夹2中没有的文件
    diff_in_folder1 = files_folder1 - files_folder2

    # 找到文件夹2中有而文件夹1中没有的文件
    diff_in_folder2 = files_folder2 - files_folder1

    # 输出不同的文件名
    if diff_in_folder1:
        print("文件夹1中有，但文件夹2中没有的文件：")
        for file in diff_in_folder1:
            print(file)

    if diff_in_folder2:
        print("文件夹2中有，但文件夹1中没有的文件：")
        for file in diff_in_folder2:
            print(file)

    if not diff_in_folder1 and not diff_in_folder2:
        print("两个文件夹中的文件名完全相同。")

# 设置文件夹路径
folder1 = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images/'  # 将其替换为第一个文件夹的路径
folder2 = '/home/yaoteam/yaoteam/wz/20250226 去大虫后10000张图片/'  # 将其替换为第二个文件夹的路径

# 检查文件夹中的文件名差异
check_diff_files(folder1, folder2)