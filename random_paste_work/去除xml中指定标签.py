import os
import xml.etree.ElementTree as ET

# 输入原始 XML 路径
xml_input_dir = '/home/yaoteam/yaoteam/wz/20250303_preds2coco_xml_已过滤/'
# 输出路径（修改后的 XML 保存处）
xml_output_dir = '/home/yaoteam/yaoteam/wz/13019图片_整合oss_去除小虫标注/xml/'
os.makedirs(xml_output_dir, exist_ok=True)

# 要删除的目标 name 列表（可扩展）
remove_names = ['insect']

for xml_file in os.listdir(xml_input_dir):
    if not xml_file.endswith('.xml'):
        continue

    xml_path = os.path.join(xml_input_dir, xml_file)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 找出所有 <object> 节点
        objects = root.findall('object')

        removed = 0
        for obj in objects:
            name_node = obj.find('name')
            if name_node is not None and name_node.text.strip() in remove_names:
                root.remove(obj)
                removed += 1

        if removed > 0:
            print(f"[处理] {xml_file}：移除 {removed} 个 'insect' 标注")

        # ✅ 无论是否还有 object，都保存
        new_path = os.path.join(xml_output_dir, xml_file)
        tree.write(new_path, encoding='utf-8', xml_declaration=True)

    except Exception as e:
        print(f"[错误] 处理 {xml_file} 时出错：{e}")