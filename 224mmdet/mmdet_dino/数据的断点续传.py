import os
import shutil
from tqdm import tqdm

def get_filenames_without_extension(directory):
    """Get a set of filenames without their extensions from a directory."""
    filenames = set()
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filenames.add(os.path.splitext(filename)[0])
    return filenames

def copy_unique_files(src_dir, dst_dir, ref_dir):
    """Copy files from src_dir to dst_dir if they are not in ref_dir (based on filename without extension)."""
    src_filenames = get_filenames_without_extension(src_dir)
    ref_filenames = get_filenames_without_extension(ref_dir)
    
    unique_filenames = src_filenames - ref_filenames
    copied_files_count = 0
    
    os.makedirs(dst_dir, exist_ok=True)
    
    for filename in tqdm(os.listdir(src_dir), desc="Copying files"):
        if os.path.splitext(filename)[0] in unique_filenames:
            src_file_path = os.path.join(src_dir, filename)
            dst_file_path = os.path.join(dst_dir, filename)
            shutil.copy2(src_file_path, dst_file_path)
            copied_files_count += 1
    
    print(f"Total copied files: {copied_files_count}")

# Usage example
src_directory = "/home/yaoteam/yaoteam/yyc/YYC_SSD/cebaodengall/JPEGImages2"
dst_directory = "/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/tmp"
ref_directory = "/home/yaoteam/yaoteam/yyc/mmdet_dino/outputs_cebaodengall2/preds"

copy_unique_files(src_directory, dst_directory, ref_directory)
