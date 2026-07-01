"""
import os
from collections import defaultdict

def count_files_with_dirs(directory):
    total_files = 0
    jpg_files = 0
    name_to_paths = defaultdict(list)  # 文件名 -> 路径列表

    for root, _, files in os.walk(directory):
        total_files += len(files)
        jpg_files += sum(1 for file in files if file.lower().endswith('.jpg'))
        for file in files:
            name, ext = os.path.splitext(file)
            name_to_paths[name].append(os.path.join(root, file))

    # 筛选重复文件名
    repeated_files = {name: paths for name, paths in name_to_paths.items() if len(paths) > 1}
    return total_files, jpg_files, name_to_paths, repeated_files

# 主程序入口
if __name__ == "__main__":
    folder_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/2024summer_biaozhu_small_img_12000"
    output_txt = "重复文件统计结果.txt"

    total, jpg_count, all_names, repeated = count_files_with_dirs(folder_path)

    # 打开 txt 文件写入
    with open(output_txt, "w", encoding="utf-8") as f:
        def log(msg):
            print(msg)
            f.write(msg + "\n")

        log(f"总文件数: {total}")
        log(f".jpg 文件数: {jpg_count}")
        log(f"唯一文件数: {len(all_names)}\n")

        log("重复文件及其所在文件夹：")
        for name, paths in repeated.items():
            log(f"\n文件名: {name}, 数量: {len(paths)}")
            for path in paths:
                parent_folder = os.path.basename(os.path.dirname(path))
                log(f" - 所在文件夹: {parent_folder}, 路径: {path}")

    print(f"\n✅ 统计完成，结果已保存到: {output_txt}") ，，现在我统计出来有很多重复文件我要对齐进行人工纠正，大致思路是，先将重复的文件复制到指定输出目录的子文件中，子文件夹名为重复文件的所有父文件夹名组合而成用@隔开；然后由人工将输出文件夹中都
"""

