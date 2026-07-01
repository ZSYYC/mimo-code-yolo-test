import os
import shutil
from tqdm import tqdm
import logging

# 设置日志记录
logging.basicConfig(filename='file_processing.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def move_images_to_class_folder(class_folder):
    """将类别子文件夹下聚类子文件夹内的所有图片提取到该类别子文件夹"""
    moved_files = 0
    failed_files = 0
    skipped_files = 0

    # 获取所有子文件夹
    subdirs = [d for d in os.listdir(class_folder) if os.path.isdir(os.path.join(class_folder, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(class_folder, subdir)

        # 递归处理所有子文件夹中的文件
        for root, _, files in os.walk(subdir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and file.lower().endswith('.jpg'):
                    target_path = os.path.join(class_folder, file)

                    # 处理文件名冲突
                    if os.path.exists(target_path):
                        base_name, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(target_path):
                            new_file = f"{base_name}_{counter}{ext}"
                            target_path = os.path.join(class_folder, new_file)
                            counter += 1
                        logging.info(f"文件名冲突，重命名为: {os.path.basename(target_path)}")
                        skipped_files += 1

                    # 使用try-except处理移动操作
                    try:
                        shutil.copy2(file_path, target_path)
                        os.remove(file_path)  # 移除原文件
                        moved_files += 1
                    except Exception as e:
                        logging.error(f"移动文件失败: {file_path} -> {target_path}, 错误: {str(e)}")
                        failed_files += 1

        # 移动完成后再删除文件夹
        try:
            shutil.rmtree(subdir_path)
            logging.info(f"删除文件夹: {subdir_path}")
        except Exception as e:
            logging.error(f"删除文件夹失败: {subdir_path}, 错误: {str(e)}")

    return moved_files, failed_files, skipped_files

def remove_non_jpg_files(class_folder):
    """删除类别文件夹下所有非 .jpg 结尾的文件"""
    removed_files = 0
    for file in os.listdir(class_folder):
        file_path = os.path.join(class_folder, file)
        if os.path.isfile(file_path) and not file.lower().endswith('.jpg'):
            try:
                os.remove(file_path)
                logging.info(f"删除非JPG文件: {file_path}")
                removed_files += 1
            except Exception as e:
                logging.error(f"删除文件失败: {file_path}, 错误: {str(e)}")
    return removed_files

def count_jpg_files(directory):
    """统计指定目录中的JPG文件数量（包括子目录）"""
    jpg_count = 0
    for root, _, files in os.walk(directory):
        jpg_count += sum(1 for file in files if file.lower().endswith('.jpg'))
    return jpg_count

def process_folder(folder_path):
    """执行所有处理步骤，并显示进度条和统计信息"""
    # 处理前计数
    before_count = count_jpg_files(folder_path)
    print(f"处理前JPG文件数: {before_count}")
    logging.info(f"处理前JPG文件数: {before_count}")

    # 获取所有类别文件夹
    class_folders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) 
                     if os.path.isdir(os.path.join(folder_path, d))]

    total_moved = 0
    total_failed = 0
    total_skipped = 0
    total_removed = 0

    print("正在处理文件...")
    for class_folder in tqdm(class_folders, desc="处理类别", unit="class"):
        moved, failed, skipped = move_images_to_class_folder(class_folder)
        removed = remove_non_jpg_files(class_folder)

        total_moved += moved
        total_failed += failed
        total_skipped += skipped
        total_removed += removed

    # 处理后计数
    after_count = count_jpg_files(folder_path)

    # 打印统计信息
    print("\n处理完成！")
    print(f"处理前JPG文件数: {before_count}")
    print(f"处理后JPG文件数: {after_count}")
    print(f"移动文件: {total_moved}")
    print(f"重命名文件: {total_skipped}")
    print(f"移动失败: {total_failed}")
    print(f"删除非JPG文件: {total_removed}")

    if before_count != after_count:
        print(f"警告：文件数量变化! 差异: {after_count - before_count}")
        logging.warning(f"文件数量变化! 处理前: {before_count}, 处理后: {after_count}, 差异: {after_count - before_count}")

if __name__ == "__main__":
    folder_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/2024summer_biaozhu_small_img_12000'
    if os.path.isdir(folder_path):
        process_folder(folder_path)
    else:
        print("无效的文件夹路径!")