from sahi.utils.coco import Coco

# init Coco object
coco = Coco.from_coco_dict_or_path("/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/annotations/val2017.json", image_dir="/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images/")

# export converted YoloV5 formatted dataset into given output_dir with a 85% train/15% val split
coco.export_as_yolov5(
  output_dir="/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/yolo_formet_dataset",
  train_split_rate=1
)

# 下面是把有train和val的coco数据集转换为yolo


# from sahi.utils.coco import Coco, export_coco_as_yolov5

# # init Coco object
# train_coco = Coco.from_coco_dict_or_path("/usr/src/ultralytics/slice_result_test_0124_shui_dao_suo_pai_she_male/sliced_coco.json", image_dir="/usr/src/ultralytics/slice_result_train_109_segment_copy_paste_1280/")
# val_coco = Coco.from_coco_dict_or_path("/usr/src/ultralytics/slice_result_train_109_segment_copy_paste_1280_test_val/sliced_coco.json", image_dir="/usr/src/ultralytics/slice_result_train_109_segment_copy_paste_1280_test_val/")

# # export converted YoloV5 formatted dataset into given output_dir with given train/val split
# data_yml_path = export_coco_as_yolov5(
#   output_dir="/usr/src/ultralytics/slice_result_train_109_segment_copy_paste_1280_yolo_datasets",
#   train_coco=train_coco,
#   val_coco=val_coco
# )
