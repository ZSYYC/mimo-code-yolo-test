import json
import os

def update_image_filenames(json_file_path):
    # 读取 COCO 数据集的 JSON 标注文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)

    # 遍历 images 键下的所有图片信息
    for image_info in coco_data['images']:
        # 获取图片的原始文件名
        original_filename = image_info['file_name']
        
        # 分离文件名和扩展名
        name, ext = os.path.splitext(original_filename)
        
        # 修改文件名后缀为 .jpg
        new_filename = name + '.jpg'
        
        # 更新文件名
        image_info['file_name'] = new_filename
        print(f"Updated: {original_filename} -> {new_filename}")
    
    # 保存修改后的内容回到原始 JSON 文件（或保存到新的文件）
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=4)
    print(f"Updated JSON saved to {json_file_path}")

# 设置 COCO JSON 文件的路径
json_file = '/home/yaoteam/yaoteam/lgz/tmp_dataset/annotations/test2017.json'

# 调用函数修改所有图片的文件名后缀
update_image_filenames(json_file)
