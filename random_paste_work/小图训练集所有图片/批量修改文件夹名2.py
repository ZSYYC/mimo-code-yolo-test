import os
import shutil

# 定义映射关系
mapping = [
    ("e9", "Q7"), ("q5", "Q6"), ("e4", "L104"), ("e3", "L59"), ("e12", "L87"),
    ("q2", "L81"), ("bbfs", "B5"), ("y4", "L2"), ("y3", "L1"), ("e2", "L47"),
    ("hfs", "B4"), ("e11", "L93"), ("q16", "Z3"), ("q1", "B14"), ("y8", "L11"),
    ("yechan", "B12"), ("q8", "L162"), ("蝼蛄", "Z1"), ("q12", "M1"), ("q14", "L43"),
    ("Cicadellidae叶蝉类", "B12"), ("q15", "Q1"), ("电光叶婵", "B12"), ("e10", "Q6"),
    ("e1", "L9"), ("e8", "L84"), ("q18", "Z1"), ("q6", "L157"), ("e5", "L41"),
    ("q10", "B19"), ("q13", "L158"), ("q17", "Q2"), ("荧叶甲类", "Q3"), ("e7", "L17"),
    ("q3", "B18"), ("q7", "L160"), ("大红蝽", "B1"), ("白薯天蛾", "L29"), ("y5", "L40"),
    ("y6", "L90"), ("Carabidae步甲类", "Q10"), ("天蛾类", "天蛾类"), ("黑尾叶蝉", "B12"),
    ("逗斑青步甲", "Q10"), ("水龟甲类", "水龟甲类"), ("电光叶蝉", "B13"), ("q4", "Q18"),
    ("q11", "B3"), ("蝗虫类", "Z2"), ("银纹夜蛾", "L10"), ("玉米螟", "L40"), ("铜绿丽金龟", "Q7"),
    ("other", "other"), ("a2", "L1"), ("人纹污灯蛾", "L34"), ("粘虫类", "L51"), ("a41", "格蔗尺蛾"),
    ("e6", "L161"), ("f124", "f124"), ("a216", "a216"), ("寄生蜂类", "寄生蜂类"), ("稻棘缘蝽", "B11"),
    ("金星尺蛾", "L23"), ("八点灰灯蛾", "L35"), ("毒蛾类", "毒蛾类"), ("g23", "g23"), ("c81", "c81"),
    ("红天蛾", "L26"), ("稻绿蝽", "B9"), ("e120", "橄榄绿尾尺蛾"), ("大螟", "L9"), ("e40", "L130"),
    ("蝉科", "蝉科"), ("蟋蟀类", "Z3"), ("a219", "a219"), ("鳃金龟类", "Q5orQ6"), ("草蛉类", "M1"),
    ("棉铃虫", "L59"), ("灯蛾类", "灯蛾类L120"), ("尺蛾科", "尺蛾科"), ("b13", "b13"), ("稻黑蝽", "B19"),
    ("d171", "d171"), ("m32", "m32")
]

# 将映射关系转换为字典
folder_mapping = dict(mapping)

def rename_and_merge_folders(input_folder):
    for sub_folder in os.listdir(input_folder):
        src_sub_folder_path = os.path.join(input_folder, sub_folder)
        
        if os.path.isdir(src_sub_folder_path):
            # 获取新的文件夹名称
            new_name = folder_mapping.get(sub_folder, sub_folder)
            dest_sub_folder_path = os.path.join(input_folder, new_name)

            if os.path.exists(dest_sub_folder_path) and src_sub_folder_path != dest_sub_folder_path:
                # 如果目标文件夹已存在，则合并内容
                for file_name in os.listdir(src_sub_folder_path):
                    src_file_path = os.path.join(src_sub_folder_path, file_name)
                    dest_file_path = os.path.join(dest_sub_folder_path, file_name)
                    
                    if not os.path.exists(dest_file_path):
                        shutil.move(src_file_path, dest_file_path)
                    else:
                        # 如果文件已存在，可以选择覆盖或跳过，当前选择跳过
                        print(f"File {dest_file_path} already exists. Skipping.")
                
                # 合并完成后，删除空的源文件夹
                os.rmdir(src_sub_folder_path)
            else:
                # 如果目标文件夹不存在，直接重命名
                os.rename(src_sub_folder_path, dest_sub_folder_path)

input_folder = '/home/yaoteam/yaoteam/yyc/random_paste_work/小图训练集所有图片/小图训练集所有已分类图片'
rename_and_merge_folders(input_folder)
