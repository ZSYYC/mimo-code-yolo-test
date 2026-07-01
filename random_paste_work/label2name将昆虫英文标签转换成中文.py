import pandas as pd

# 读取CSV文件
csv_file = '/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi.csv'
df = pd.read_csv(csv_file)

# 创建标签映射字典
label_mapping = dict(zip(df['ret'], df['name']))

# 给定的标签变量
labels = ['L60', 'L17', 'L89', 'L7', 'L3', 'L59', 'L16', 'L47', 'B4', 'B12', 'B33', 'B5', 'B40', 'B13', 'L41', 'L18', 'L1', 'B17', 'Q7', 'L37', 'B7', 'L2', 'L12', 'L35', 'L23', 'L43', 'L28', 'L15', 'L8', 'L29', 'L9', 'B18', 'B15', 'Q50', 'B6', 'L21', 'L27', 'B14', 'L13', 'L4', 'Q60', 'B1', 'L159', 'Q26', 'L191', 'Q12', 'L152', 'L46', 'L5', 'L215', 'Q4']
labels = ['B16']
# 转换标签为中文名称
converted_labels = {label: label_mapping[label] if label in label_mapping else label for label in labels}

print(converted_labels)