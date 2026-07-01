from PIL import Image, ImageDraw
import json
import os
from tqdm import tqdm

def load_annotations(json_file):
    with open(json_file) as file:
        data = json.load(file)
    return data

def cut_and_save_objects(image, annotations, output_dir, image_id, xml_file):
    for annotation in annotations:
        if annotation['image_id'] == image_id and annotation.get('segmentation'):
            # 初始化一个空的掩码以合并所有多边形
            mask = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask)
            has_valid_segmentation = False

            for segment in annotation['segmentation']:
                # 确保坐标列表至少有两个坐标点
                if len(segment) >= 6:  # 需要至少三个点来绘制一个多边形
                    polygon = [(segment[i], segment[i + 1]) for i in range(0, len(segment), 2)]
                    draw.polygon(polygon, fill=255)  # 确保多边形内部是不透明的
                    has_valid_segmentation = True

            if has_valid_segmentation:
                # 使用掩码提取对象
                cropped_object = image.copy()
                cropped_object.putalpha(mask)

                # 裁剪到边界框大小
                bbox = annotation['bbox']
                cropped_object = cropped_object.crop((bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]))

                # 保存裁剪对象
                cropped_object.save(os.path.join(output_dir, f"{os.path.basename(xml_file)[:-4]}" + f"_{bbox[0]}_{bbox[1]}_{bbox[0]+bbox[2]}_{bbox[1]+bbox[3]}.png"), "PNG")
            else:
                print(f"Skipping annotation {annotation['id']} due to insufficient coordinates.")
  

json_file = "/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/掩膜标注.json"
image_dir = "/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/抽样数据集/JPEGImages"
output_dir = "/home/yaoteam/yaoteam/yyc/A关于groundingsam实验0729/crop_mask_img"

annotations = load_annotations(json_file)
# count = 0
for image_info in tqdm(annotations['images']):
    # count +=1
    # if count==2:
    #     break
    image_path = os.path.join(image_dir, image_info['file_name'])
    image = Image.open(image_path)
    cut_and_save_objects(image, annotations['annotations'], output_dir, image_info['id'],image_info['file_name'])
