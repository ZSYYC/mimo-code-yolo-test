import os
import xml.etree.ElementTree as ET
from pathlib import Path

def update_xml_file(xml_path, new_filename, new_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Update <filename> tag
    filename_tag = root.find('filename')
    if filename_tag is not None:
        filename_tag.text = new_filename
    
    # Update <path> tag
    path_tag = root.find('path')
    if path_tag is not None:
        path_tag.text = new_path
    
    # Write changes back to the XML file
    tree.write(xml_path)

def rename_files_and_update_xml(folder_path):
    annotations_folder = os.path.join(folder_path, 'Annotations')
    images_folder = os.path.join(folder_path, 'JPEGImages')
    
    xml_files = sorted(Path(annotations_folder).glob('*.xml'))
    image_files = sorted(Path(images_folder).glob('*.*'))
    
    if len(xml_files) != len(image_files):
        print("Number of XML files and image files do not match!")
        return
    
    for i, (xml_file, image_file) in enumerate(zip(xml_files, image_files)):
        new_name = f"{i+1}"
        new_image_filename = f"{new_name}{image_file.suffix}"
        new_image_path = os.path.join(images_folder, new_image_filename)
        
        new_xml_filename = f"{new_name}.xml"
        new_xml_path = os.path.join(annotations_folder, new_xml_filename)
        
        # Rename image file
        os.rename(image_file, new_image_path)
        
        # Rename XML file
        os.rename(xml_file, new_xml_path)
        
        # Update XML content
        update_xml_file(new_xml_path, new_image_filename, new_image_path)
        
        if i % 1000 == 0:
            print(f"Processed {i+1} files")

if __name__ == "__main__":
    folder_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/voc2coco/VOC"  # Replace with the path to your folder
    rename_files_and_update_xml(folder_path)
