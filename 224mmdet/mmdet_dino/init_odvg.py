import os
import cv2
import json
import jsonlines

data_root = 'data/img_cebaodeng_pseudo'
images_path = os.path.join(data_root, 'images')
out_path = os.path.join(data_root, 'insect_train_od.json')
metas = []
for files in os.listdir(images_path):
    img = cv2.imread(os.path.join(images_path, files))
    height, width, _ = img.shape
    metas.append({"filename": files, "height": height, "width": width})

with jsonlines.open(out_path, mode='w') as writer:
    writer.write_all(metas)

# 生成 label_map.json，由于只有一个类别，所以只需要写一个 cat 即可
label_map_path = os.path.join(data_root, 'insect_label_map.json')
with open(label_map_path, 'w') as f:
    json.dump({'0': 'insect'}, f)