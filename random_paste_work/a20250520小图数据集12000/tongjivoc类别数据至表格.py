import csv
import os
import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict

def build_name_ret_dict(csv_path):
    name_ret_map = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].strip()
            ret = row['ret'].strip()
            name_ret_map[name] = ret
    return name_ret_map

# 原始类别中文名到标签的映射（部分示例，请替换为完整映射）
name_ret_map = build_name_ret_dict('/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/ser_insect_permi.csv')
# 反转映射：标签 => 中文名
label_to_chinese = {v: k for k, v in name_ret_map.items()}

def count_voc_labels_from_folders(xml_folders):
    label_count = defaultdict(int)

    for folder in xml_folders:
        for filename in os.listdir(folder):
            if filename.endswith('.xml'):
                file_path = os.path.join(folder, filename)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    for obj in root.findall('object'):
                        name = obj.find('name').text.strip()
                        label_count[name] += 1
                except Exception as e:
                    print(f"Failed to parse {file_path}: {e}")

    return label_count

# VOC XML 文件夹路径列表（可添加多个）
xml_folders = [
    '/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/outputs/测报灯图片0724/抽样出目标数大于5的图片2000张/xml',
    '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/xml汇总20250225'
]

# 统计标签数量
label_count_dict = count_voc_labels_from_folders(xml_folders)

# 构造 DataFrame
data = []
for label, count in label_count_dict.items():
    chinese_name = label_to_chinese.get(label, label)  # 如果找不到就用标签代替
    data.append((chinese_name, label, count))

df = pd.DataFrame(data, columns=['类别中文名', '类别标签', '数量'])
df = df.sort_values(by='数量', ascending=False)

# 保存 Excel
output_excel = '/home/yaoteam/yaoteam/yyc/random_paste_work/a20250520小图数据集12000/12000张数据集回溯结果统计.xlsx'
df.to_excel(output_excel, index=False)

# 输出汇总信息
print(f"Total unique labels: {len(df)}")
print(f"Statistics saved to {output_excel}")
