import pandas as pd
import os
# 读取CSV文件
csv_file = '/home/yaoteam/yaoteam/yyc/mmdet_dino/ser_insect_permi.csv'
df = pd.read_csv(csv_file)

# 创建标签映射字典
label_mapping = dict(zip(df['ret'], df['name']))

def count_files_in_folders(input_folder):
    # 初始化计数器
    folder_file_count = {}
    total_files = 0
    total_folders = 0

    # 遍历input_folder中的每个子文件夹
    for sub_folder in os.listdir(input_folder):
        sub_folder_path = os.path.join(input_folder, sub_folder)
        
        if os.path.isdir(sub_folder_path):
            total_folders += 1
            file_count = len([f for f in os.listdir(sub_folder_path) if os.path.isfile(os.path.join(sub_folder_path, f))])
            folder_file_count[sub_folder] = file_count
            total_files += file_count

    return folder_file_count

# 指定input_folder路径
input_train_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train3000/train'
input_val_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/何工纠正一二类害虫数据集/train3000/val'

# 统计文件数量
train_folder_file_count = count_files_in_folders(input_train_folder)
val_folder_file_count = count_files_in_folders(input_val_folder)

# 定义函数读取txt文件并生成Excel
def txt_to_excel(txt_file, excel_file):
    # 读取txt文件，假设每行数据由' :'分隔
    data = []
    with open(txt_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:  # 忽略空行
                class_name, num = line.split(' :')
                class_label, _ = class_name.split('@')
                # print(num)
                precision, recall, f1 = num.split()
                class_name = class_name.strip()
                precision, recall, f1 = map(float, [precision.strip(), recall.strip(), f1.strip()])
                data.append([class_label, label_mapping.get(class_label, class_label),train_folder_file_count[class_label], val_folder_file_count[class_label], precision, recall, f1])

    # 使用 pandas 创建 DataFrame
    df = pd.DataFrame(data, columns=['label', 'Classes', 'train', 'test', 'Precision %', 'Recall %', 'F1 %'])

    # 保存为 Excel 文件
    df.to_excel(excel_file, index=False, engine='openpyxl')


# 使用函数读取 txt 并生成 Excel 文件
txt_file = r'/home/yaoteam/yaoteam/yyc/random_paste_work/分类模型数据集精度统计20250225/swinb分类模型准确率.txt'  # 输入你的 txt 文件路径
excel_file = r'/home/yaoteam/yaoteam/yyc/random_paste_work/分类模型数据集精度统计20250225/output.xlsx'  # 输出的 Excel 文件路径

txt_to_excel(txt_file, excel_file)

print("Excel 文件已生成！")
