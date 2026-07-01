import collections
import csv
import heapq
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import Counter

def get_result(pred_result, txt_names, thr = 0.99, min_prob = 1e-9)-> tuple[str, float]:
    probs = pred_result[0]['pred_scores'] # 预测的分数
    probs = torch.from_numpy(probs) # 转换为tensor
    pred_score = pred_result[0]['pred_score'] # 预测的置信度
    pred_class = pred_result[0]['pred_class'] # 预测的物种
    # 如果到物种的预测置信度大于thr直接返回
    if pred_score >= thr:
        return pred_class, pred_score

    rank_index = 6-1 # 物种级别的索引,从属开始统计
    while True:
        output = collections.defaultdict(float) # 当访问不存在的键时，返回0.0，而不是抛出异常Key
        for i in torch.nonzero(probs > min_prob).squeeze():
            i = i.item() if isinstance(i, torch.Tensor) else i
            output[txt_names[i][rank_index]] += probs[i].item()

        top1_txt_name = heapq.nlargest(1, output, key=output.get) # 从字典 output 中根据值（output.get）提取出值最大的键，并返回一个包含该键的列表。
        pred_score = output[top1_txt_name[0]]
        rank_index -= 1
        if pred_score >= thr or rank_index < 0:
            return top1_txt_name[0], pred_score

nparr = np.array([3.6357035e-04, 3.8756005e-04, 2.6755332e-04, 4.5339650e-04,
       3.7039342e-04, 4.3424091e-04, 2.7942928e-04, 3.5226787e-04,
       7.8163733e-04, 4.5278724e-04, 3.7674740e-04, 5.1291782e-04,
       5.0940609e-04, 3.6422105e-04, 3.9465583e-04, 4.6386771e-04,
       3.4327214e-04, 3.7593502e-04,..., 4.0632029e-04, 3.0712620e-04,
       2.7011865e-04, 5.1631703e-04, 3.0849632e-04, 3.6824317e-04,
       4.3667672e-04, 4.3458829e-04, 2.6830120e-04, 3.5545373e-04,
       3.9706251e-04, 2.9435876e-04, 4.1635914e-04, 3.5235690e-04,
       2.2432394e-04, 4.0394181e-04, 3.8249788e-04, 4.1279563e-04,
       4.1587913e-04, 4.3486748e-04, 4.3800386e-04, 7.5704505e-04], dtype=np.float32)

mock_result = [{'pred_scores':nparr, 'pred_label': 43, 'pred_score': 0.7835080623626709, 'pred_class': 'L11'}]

insect_class_list = ['B1', 'B10', 'B12', 'B13', ..., 'B9', 'FL2', 'FY1', 'G1', 'L1', 'L10', 'L103', 'L104', 'L11', 'L112', 'L115', 'L120', 'L123', 'L126', 'L127', 'L129', 'L13', 'L130', 'L14', 'L145', 'L15', 'L152', 'L156', 'L157', 'L159', 'L16', 'L160', 'L161', 'L164', 'L165', 'L169', 'L17', 'L170', 'L18', 'L182', 'L184', 'L185', 'L186', 'L187', 'L188', 'L191', 'L192', 'L193', 'L194', 'L197', 'L199', 'L2', 'L20', 'L200', 'L201', 'L202', 'L203', 'L204', 'L206', 'L209', 'L21', 'L211', 'L212', 'L213', 'L214', 'L215', 'L216', 'L217', 'L218', 'L22', 'L227', 'L229', 'L23', 'L24', 'L25', 'L26', 'L27', 'L28', 'L29', 'L3', 'L30', 'L31', 'L33', 'L330', 'L332', 'L336', 'L337', 'L338', 'L339', 'L34', 'L340', 'L341', 'L343', 'L344', 'L345', 'L346', 'L347', 'L349', 'L35', 'L350', 'L352', 'L353', 'L36', 'L37', 'L371', 'L372', 'L373', 'L374', 'L38', 'L39', 'L4', 'L40', 'L41', 'L42', 'L43', 'L46', 'L47', 'L53', 'L58', 'L59', 'L6', 'L60', 'L63', 'L64', 'L67', 'L72', 'L73', 'L74', 'L75', 'L81', 'L82', 'L84', 'L85', 'L86', 'L87', 'L9', 'L90', 'L93', 'L94', 'L96', 'L98', 'M1', 'M2', 'M4', 'MAO1', 'MAO2', 'MO2', 'MO3', 'MO4', 'MO5', 'MO6', 'MO7', 'MO8', 'N1', 'Q1', 'Q10', 'Q11', 'Q12', 'Q13', 'Q25', 'Q26', 'Q29', 'Q30', 'Q31', 'Q33', 'Q34', 'Q35', 'Q37', 'Q39', 'Q4', 'Q40', 'Q44', 'Q45', 'Q47', 'Q48', 'Q49', 'Q50', 'Q51', 'Q53', 'Q54', 'Q55', 'Q56', 'Q57', 'Q58', 'Q59', 'Q60', 'Q62', 'Q63', 'Q64', 'Q65', 'Q67', 'Q7', 'QT1', 'S2', 'S3', 'S4', 'S6', 'S7', 'S8', 'S9', 'Z1', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'olegs']


txt_names = []
with open(r'D:\A_finallshell_download\ser_insect_permi_update.csv', mode='r', newline='', encoding='utf-8-sig') as file:
    reader = list(csv.reader(file))
    reader = reader[1:]  # 跳过表头

for insect_class in insect_class_list:
    for row in reader:
        # _id,Species,Genus,Family,Order,Class,Phylum,Kingdom,_ret,_color
        # 1,二化螟,二化螟属,螟蛾科,鳞翅目,昆虫纲,节肢动物门,动物界,L1,#000000
        if row[-2] == insect_class:
            # 添加到数组
            txt_names.append([row[-3], row[-4], row[-5], row[-6], row[-7], row[-8], row[-9]])
            break
        if row[0]==reader[-1][0]:
            print(f'未找到{insect_class}!请补全之后再运行！') 
if len(txt_names) != len(insect_class_list):
    raise ValueError(f'未找到{len(insect_class_list)-len(txt_names)}个！请补全之后再运行！')       


print(get_result(mock_result, txt_names))


