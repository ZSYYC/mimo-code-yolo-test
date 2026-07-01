import torch

# # 加载官方预训练权重
# pretrained_weights = torch.load('/home/yaoteam/yaoteam/yyc/Swin-Transformer/swin_tiny_patch4_window7_224.pth')

# # 提取官方模型中的参数
# official_model_weights = pretrained_weights['model']

# # 创建新的权重字典，包含两个自监督模型的主干参数
# new_weights = {'model': {}}

# # 将官方权重复制到新的权重字典中
# for key in official_model_weights.keys():
#     # 转换encoder的权重
#     if key=='head.weight' or key=='head.bias':
#         continue
#     new_weights['model'][f'encoder.{key}'] = official_model_weights[key]
# for key in official_model_weights.keys():
#     # 转换encoder_k的权重
#     if key=='head.weight' or key=='head.bias':
#         continue
#     new_weights['model'][f'encoder_k.{key}'] = official_model_weights[key]

# # 保存新的权重文件
# torch.save(new_weights, '/home/yaoteam/yaoteam/yyc/cuda1130-cudnn8-devel-ubuntu20.04/moby_swin_t.pth')

# print("转换完成，新的权重文件已保存。")




pretrained_weights = torch.load('/home/yaoteam/yaoteam/yyc/mmpretrain/mocov3_vitb300/epoch_219.pth', map_location="cpu")
# pretrained_weights = torch.load('/home/yaoteam/yaoteam/yyc/Swin-Transformer/swin_tiny_patch4_window7_224.pth', map_location="cpu")
# Print the keys of the state dict
for key in pretrained_weights.keys():
    print(key)
print("{0:=^60}".format("keys"))
for key in pretrained_weights.keys():
    for keys in pretrained_weights[key].keys():
        print(keys)
    print("{0:=^60}".format(f'{key}'))