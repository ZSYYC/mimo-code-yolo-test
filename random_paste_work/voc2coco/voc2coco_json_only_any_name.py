import os
import json
import shutil
import random
import xml.etree.ElementTree as ET
import glob

START_BOUNDING_BOX_ID = 1
PRE_DEFINE_CATEGORIES = None

def get(root, name):
    vars = root.findall(name)
    return vars

def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise ValueError(f"Cannot find {name} in {root.tag}.")
    if length > 0 and len(vars) != length:
        raise ValueError(
            f"The size of {name} is supposed to be {length}, but is {len(vars)}."
        )
    if length == 1:
        vars = vars[0]
    return vars

def get_filename(filename):
    filename = filename.replace("\\", "/")
    return os.path.basename(filename)

def get_categories(xml_files):
    classes_names = []
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall("object"):
            classes_names.append(member[0].text)
    classes_names = list(set(classes_names))
    classes_names.sort()
    print(f"类别名字为{classes_names}")
    return {name: i for i, name in enumerate(classes_names)}

def convert(xml_files, json_file):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    if PRE_DEFINE_CATEGORIES is not None:
        categories = PRE_DEFINE_CATEGORIES
    else:
        categories = get_categories(xml_files)
    bnd_id = START_BOUNDING_BOX_ID
    image_id = 1  # Initialize image_id here
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        path = get(root, "path")
        if len(path) == 1:
            # print(path[0].text)
            filename = os.path.basename(path[0].text)
        elif len(path) == 0:
            filename = get_and_check(root, "filename", 1).text
        else:
            raise ValueError("%d paths found in %s" % (len(path), xml_file))
        
        filename = get_filename(filename)  # Use the modified function
        size = get_and_check(root, "size", 1)
        width = int(get_and_check(size, "width", 1).text)
        height = int(get_and_check(size, "height", 1).text)
        image = {
            "file_name": filename,
            "height": height,
            "width": width,
            "id": image_id,  # Use the unique image_id
        }
        json_dict["images"].append(image)
        
        for obj in get(root, "object"):
            category = get_and_check(obj, "name", 1).text
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, "bndbox", 1)
            xmin = round(float(get_and_check(bndbox, "xmin", 1).text)) - 1
            ymin = round(float(get_and_check(bndbox, "ymin", 1).text)) - 1
            xmax = round(float(get_and_check(bndbox, "xmax", 1).text))
            ymax = round(float(get_and_check(bndbox, "ymax", 1).text))
            assert xmax > xmin
            assert ymax > ymin
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {
                "area": o_width * o_height,
                "iscrowd": 0,
                "image_id": image_id,
                "bbox": [xmin, ymin, o_width, o_height],
                "category_id": category_id,
                "id": bnd_id,
                "ignore": 0,
                "segmentation": [],
            }
            json_dict["annotations"].append(ann)
            bnd_id += 1
        
        image_id += 1  # Increment the unique image_id

    for cate, cid in categories.items():
        cat = {"supercategory": "none", "id": cid, "name": cate}
        json_dict["categories"].append(cat)

    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    with open(json_file, "w") as json_fp:
        json_str = json.dumps(json_dict)
        json_fp.write(json_str)

def mkdir(path):
    path = path.strip().rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' ----- folder created')
        return True
    else:
        print(path + ' ----- folder existed')
        return False

def main(voc_annotations, valRatio, testRatio, main_path):
    xmlNum = len(os.listdir(voc_annotations))
    val_files_num = int(xmlNum * valRatio)
    test_files_num = int(xmlNum * testRatio)

    coco_path = main_path
    coco_json_annotations = os.path.join(coco_path, 'annotations')
    xml_val = os.path.join(main_path, 'xml', 'xml_val')
    xml_test = os.path.join(main_path, 'xml', 'xml_test')
    xml_train = os.path.join(main_path, 'xml', 'xml_train')

    mkdir(coco_path)
    mkdir(coco_json_annotations)
    mkdir(xml_val)
    mkdir(xml_test)
    mkdir(xml_train)

    for i in os.listdir(voc_annotations):
        xml_path = os.path.join(voc_annotations, i)
        shutil.copy(xml_path, xml_train)

    for i in range(val_files_num):
        if len(os.listdir(xml_train)) > 0:
            random_file = random.choice(os.listdir(xml_train))
            source_file = os.path.join(xml_train, random_file)
            if random_file not in os.listdir(xml_val):
                shutil.move(source_file, xml_val)
            else:
                random_file = random.choice(os.listdir(xml_train))
                source_file = os.path.join(xml_train, random_file)
                shutil.move(source_file, xml_val)
        else:
            print(f'The folders are empty, please make sure there are enough {val_files_num} files to move')
            break

    for i in range(test_files_num):
        if len(os.listdir(xml_train)) > 0:
            random_file = random.choice(os.listdir(xml_train))
            source_file = os.path.join(xml_train, random_file)
            if random_file not in os.listdir(xml_test):
                shutil.move(source_file, xml_test)
            else:
                random_file = random.choice(os.listdir(xml_train))
                source_file = os.path.join(xml_train, random_file)
                shutil.move(source_file, xml_test)
        else:
            print(f'The folders are empty, please make sure there are enough {test_files_num} files to move')
            break

    xml_val_files = glob.glob(os.path.join(xml_val, "*.xml"))
    xml_test_files = glob.glob(os.path.join(xml_test, "*.xml"))
    xml_train_files = glob.glob(os.path.join(xml_train, "*.xml"))

    convert(xml_val_files, os.path.join(coco_json_annotations, 'val2017.json'))
    convert(xml_train_files, os.path.join(coco_json_annotations, 'train2017.json'))
    if testRatio:
        convert(xml_test_files, os.path.join(coco_json_annotations, 'test2017.json'))

    try:
        shutil.rmtree(xml_train)
        shutil.rmtree(xml_val)
        shutil.rmtree(xml_test)
        shutil.rmtree(os.path.join(main_path, 'xml'))
    except:
        print(f'xml文件删除失败，请手动删除{xml_train, xml_val, xml_test}')

    print("\n\n" + "*" * 27 + "[ Done ! Go check your file ]" + "*" * 28)

if __name__ == '__main__':
    voc_annotations = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/论文用微小昆虫数据集100/10/xml1'
    valRatio = 1.0
    testRatio = 0.0
    main_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/论文用微小昆虫数据集100/10' # 跟JPEG目录同级
    main(voc_annotations, valRatio, testRatio, main_path)
