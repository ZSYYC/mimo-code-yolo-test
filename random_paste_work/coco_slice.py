from sahi.slicing import slice_coco

coco_annotation_file_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/yyc拍的飞虱数据集/原图数据集/train2017.json"
image_path = "/home/yaoteam/yaoteam/yyc/random_paste_work/yyc拍的飞虱数据集/原图数据集/img"

# 保存的coco数据集标注文件名
output_coco_annotation_file_name="sliced"
# 输出文件夹
output_dir = "/home/yaoteam/yaoteam/yyc/random_paste_work/yyc拍的飞虱数据集/裁切数据集"

# 切分数据集
coco_dict, coco_path = slice_coco(
    coco_annotation_file_path=coco_annotation_file_path,
    image_dir=image_path,
    output_coco_annotation_file_name=output_coco_annotation_file_name,
    ignore_negative_samples=True, # 是否忽略没有标注框的子图
    output_dir=output_dir,
    slice_height=1024,
    slice_width=1024,
    overlap_height_ratio=0.10,
    overlap_width_ratio=0.10,
    min_area_ratio=0.10, # 如果没有设置slice_height和slice_width，则自动确定slice_height、slice_width、overlap_height_ratio、overlap_width_ratio
    verbose=False # 是否打印详细信息
)

print("切分子图{}张".format(len(coco_dict['images'])))
print("获得标注框{}个".format(len(coco_dict['annotations'])))
