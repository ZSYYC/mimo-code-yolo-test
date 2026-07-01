import os
import shutil
import xml.etree.ElementTree as ET
from tqdm import tqdm

def move_files_without_or_single_object(img_dir, xml_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all XML files
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith(".xml")]

    # Initialize counter for moved files
    moved_files_count = 0

    # Iterate over XML files with a progress bar
    for xml_file in tqdm(xml_files, desc="Processing XML files"):
        xml_path = os.path.join(xml_dir, xml_file)
        img_path = os.path.join(img_dir, xml_file.replace('.xml', '.jpg'))

        try:
            # Parse the XML annotation file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Count the number of objects
            objects = root.findall('object')
            num_objects = len(objects)

            if num_objects == 0 :
                # Move the XML file and corresponding image file to the output directory
                shutil.move(xml_path, os.path.join(output_dir, xml_file))
                if os.path.exists(img_path):
                    shutil.move(img_path, os.path.join(output_dir, os.path.basename(img_path)))
                moved_files_count += 1
        except ET.ParseError as e:
            print(f"Error parsing {xml_path}: {e}")

    # Print the total number of moved files
    print(f"Total number of moved files: {moved_files_count}")

# Define paths
img_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/网站/其他几个测报灯图片'
xml_dir = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/xml'
output_dir = '/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/分离出来的背景图及其标注文件'

# Move files
move_files_without_or_single_object(img_dir, xml_dir, output_dir)
