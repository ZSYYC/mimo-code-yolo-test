import os
import random
import shutil
from glob import glob

def split_voc_dataset(img_dir, xml_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Split VOC dataset into training, validation, and test sets.
    
    Args:
        img_dir (str): Path to the folder containing images.
        xml_dir (str): Path to the folder containing XML annotations.
        output_dir (str): Path to the output directory.
        train_ratio (float): Proportion of data to use for training (default: 0.7).
        val_ratio (float): Proportion of data to use for validation (default: 0.2).
        test_ratio (float): Proportion of data to use for testing (default: 0.1).
    """
    assert train_ratio + val_ratio + test_ratio == 1.0, "Train, val, and test ratios must sum to 1.0"
    
    # Create output directories for train, val, and test sets
    train_img_dir = os.path.join(output_dir, 'train', 'images')
    val_img_dir = os.path.join(output_dir, 'val', 'images')
    test_img_dir = os.path.join(output_dir, 'test', 'images')
    train_xml_dir = os.path.join(output_dir, 'train', 'annotations')
    val_xml_dir = os.path.join(output_dir, 'val', 'annotations')
    test_xml_dir = os.path.join(output_dir, 'test', 'annotations')

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(test_img_dir, exist_ok=True)
    os.makedirs(train_xml_dir, exist_ok=True)
    os.makedirs(val_xml_dir, exist_ok=True)
    os.makedirs(test_xml_dir, exist_ok=True)

    # Get all image files (assuming .jpg or .png format)
    img_files = glob(os.path.join(img_dir, '*.jpg')) + glob(os.path.join(img_dir, '*.png'))
    
    # Shuffle the data
    random.shuffle(img_files)
    
    # Split the data
    total_imgs = len(img_files)
    train_cutoff = int(train_ratio * total_imgs)
    val_cutoff = int((train_ratio + val_ratio) * total_imgs)
    
    train_files = img_files[:train_cutoff]
    val_files = img_files[train_cutoff:val_cutoff]
    test_files = img_files[val_cutoff:]

    def copy_files(file_list, img_output_dir, xml_output_dir):
        for img_file in file_list:
            # Copy the image file
            shutil.move(img_file, img_output_dir)
            
            # Copy the corresponding XML file
            basename = os.path.basename(img_file)
            xml_file = os.path.join(xml_dir, basename.replace('.jpg', '.xml').replace('.png', '.xml'))
            if os.path.exists(xml_file):
                shutil.move(xml_file, xml_output_dir)
            else:
                print(f"Warning: Corresponding XML file for {img_file} not found.")

    # Copy training files
    copy_files(train_files, train_img_dir, train_xml_dir)
    
    # Copy validation files
    copy_files(val_files, val_img_dir, val_xml_dir)
    
    # Copy test files
    copy_files(test_files, test_img_dir, test_xml_dir)

    print(f"Dataset split complete. Total: {total_imgs} images.")
    print(f"Train: {len(train_files)}, Val: {len(val_files)}, Test: {len(test_files)}")

# Example usage
img_dir = "/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/JPEGImages"
xml_dir = "/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/Annotations"
output_dir = "/home/yaoteam/yaoteam/yyc/yolov8/稻飞虱数据清洗2/train_dataset"

split_voc_dataset(img_dir, xml_dir, output_dir, train_ratio=0.7, val_ratio=0.1, test_ratio=0.2)
