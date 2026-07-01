import os

def check_mismatched_files(image_folder, xml_folder):
    # 获取图片文件夹和xml文件夹中的所有文件
    image_files = set(os.path.splitext(f)[0] for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f)))
    xml_files = set(os.path.splitext(f)[0] for f in os.listdir(xml_folder) if os.path.isfile(os.path.join(xml_folder, f)))

    # 找到与图片文件夹不匹配的XML文件
    unmatched_xml_files = xml_files - image_files
    unmatched_image_files = image_files - xml_files

    # 打印结果
    if unmatched_xml_files:
        print("不匹配的XML文件:")
        for file in unmatched_xml_files:
            print(file + ".xml")
    else:
        print("所有的XML文件都有对应的图片。")

    if unmatched_image_files:
        print("不匹配的图片文件:")
        for file in unmatched_image_files:
            print(file + ".jpg")  # 假设图片的后缀是 .jpg，根据需要修改
    else:
        print("所有的图片文件都有对应的XML文件。")

# 指定图片文件夹和XML文件夹路径
image_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images_for_small_targets'
xml_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images_for_small_targets_xml'

# 调用函数进行检查
check_mismatched_files(image_folder, xml_folder)