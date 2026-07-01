import os
import csv
import shutil

def build_name_ret_dict(csv_path):
    name_ret_map = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].strip()
            ret = row['ret'].strip()
            name_ret_map[name] = ret
    return name_ret_map

def process_dataset(dataset_dir, name_ret_map):
    unmatched = []
    invalid = []

    for folder in os.listdir(dataset_dir):
        folder_path = os.path.join(dataset_dir, folder)
        if not os.path.isdir(folder_path):
            continue  # 跳过非目录

        if '@' not in folder:
            invalid.append(folder)
            continue

        name = folder.split('@', 1)[1].strip()
        if name in name_ret_map:
            ret = name_ret_map[name]
            new_folder_path = os.path.join(dataset_dir, ret)
            if not os.path.exists(new_folder_path):
                shutil.move(folder_path, new_folder_path)
            else:
                print(f"⚠️ 目标文件夹已存在，跳过重命名: {new_folder_path}")
        else:
            unmatched.append(folder)

    return unmatched, invalid

if __name__ == "__main__":
    csv_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/ser_insect_permi.csv"
    dataset_dir = "/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/2024summer_biaozhu_small_img_12000"

    name_ret_map = build_name_ret_dict(csv_path)
    print(f'{name_ret_map=}')
    # unmatched, invalid = process_dataset(dataset_dir, name_ret_map)

    # if unmatched:
    #     print("\n未匹配到 CSV 的类别（请人工处理）:")
    #     for name in unmatched:
    #         print(" -", name)

    # if invalid:
    #     print("\n不符合命名规范（缺少 @）的文件夹:")
    #     for name in invalid:
    #         print(" -", name)
