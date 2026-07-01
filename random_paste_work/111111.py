import os

# 设置你的图片和xml所在的文件夹
img_dir = '/home/yaoteam/yaoteam/wz/12000图片及其对应xml/JPGImages/'
xml_dir = '/home/yaoteam/yaoteam/wz/12000图片及其对应xml/Annotations/'

# 获取所有图片和xml的文件名（去掉后缀）
img_files = {os.path.splitext(f)[0] for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))}
xml_files = {os.path.splitext(f)[0] for f in os.listdir(xml_dir) if f.lower().endswith('.xml')}

# 找出没有对应xml的图片
no_xml_imgs = img_files - xml_files

print(f"发现 {len(no_xml_imgs)} 张没有对应XML的图片：")
for img in no_xml_imgs:
    img_path = os.path.join(img_dir, img + '.jpg')  # 假设你的图片是.jpg结尾
    if not os.path.exists(img_path):
        img_path = os.path.join(img_dir, img + '.png')  # 如果是.png
    if os.path.exists(img_path):
        confirm = input(f"确定要删除 {img_path}？(y/n): ")
        if confirm.lower() == 'y':
            os.remove(img_path)
    else:
        print(f"未找到图片文件：{img}")

print("处理完毕！")