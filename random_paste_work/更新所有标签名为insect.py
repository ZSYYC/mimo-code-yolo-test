import os
import xml.etree.ElementTree as ET

def modify_class_names(voc_annotations_path, new_class_name="insect"):
    # Get a list of all XML files in the given directory
    xml_files = [os.path.join(voc_annotations_path, f) for f in os.listdir(voc_annotations_path) if f.endswith('.xml')]
    
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Iterate over all object elements and change their class name
        for obj in root.findall('object'):
            name = obj.find('name')
            name.text = new_class_name
        
        # Write the changes back to the XML file
        tree.write(xml_file)
        print(f"Modified {xml_file}")

if __name__ == '__main__':
    voc_annotations_path = '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/insect_xml'  # Update this to your actual path
    modify_class_names(voc_annotations_path)
