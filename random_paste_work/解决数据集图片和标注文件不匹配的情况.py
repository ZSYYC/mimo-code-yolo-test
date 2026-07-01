import os

# 定义路径
images_dir = '/home/yaoteam/yaoteam/wz/voc2coco/COCO/small_insect_train'
annotations_dir = '/home/yaoteam/yaoteam/wz/voc2coco/xml/small_insect_xml_train/'

# 获取图片文件和标注文件列表
image_files = set(f.split('.')[0] for f in os.listdir(images_dir) if f.endswith('.jpg'))
annotation_files = set(f.split('.')[0] for f in os.listdir(annotations_dir) if f.endswith('.xml'))

# 找出没有对应标注文件的图片
missing_annotations = image_files - annotation_files
missing_image = annotation_files - image_files

if missing_image:
    print("Images without corresponding image:")
    for image in missing_image:
        print(image + '.xml')
else:
    print("All images have corresponding annotations.")

# 打印缺失标注文件的图片文件名
if missing_annotations:
    print("Images without corresponding annotations:")
    for image in missing_annotations:
        print(image + '.jpg')
else:
    print("All images have corresponding annotations.")
