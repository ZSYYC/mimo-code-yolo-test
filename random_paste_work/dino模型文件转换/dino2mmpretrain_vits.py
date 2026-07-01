import torch

def remove_prefix_from_state_dict(state_dict, prefix='backbone.'):
    """
    移除state_dict中键的指定前缀。
    """
    new_state_dict = {}
    for k, v in state_dict.items():
        if k.startswith(prefix):
            # 移除前缀
            new_key = k[len(prefix):]
            new_state_dict[new_key] = v
        else:
            # 如果键不以指定前缀开头，保持不变
            new_state_dict[k] = v
    return new_state_dict

def filter_and_save_weights(checkpoint, prefix_to_keep, output_pth_path):
    # Load the original .pth file
    
    # Extract state_dict
    state_dict = checkpoint['state_dict']
    # 创建新的权重字典，包含两个自监督模型的主干参数
    new_weights = {'state_dict': {}}

    for key in state_dict.keys():
        # 转换encoder的权重
        if key.startswith(prefix_to_keep):
            new_weights['state_dict'][f'{key}'] = state_dict[key]    
    # Save the new checkpoint
    torch.save(new_weights, output_pth_path)
    
    print(f"Filtered state_dict saved to {output_pth_path}")

def convert_torch_hub_to_MoCoV3(checkpoint, prefix_to_keep, output_pth_path):
    state_dict = checkpoint['teacher']
    # 创建新的权重字典，包含两个自监督模型的主干参数
    new_weights = {}

    for key in state_dict.keys():
        # 转换encoder的权重
        if key.startswith(prefix_to_keep):
            new_weights[f'{key}'] = state_dict[key]    
    target_state_dict = {'state_dict': {}}
    for key, value in new_weights.items():
        # Convert backbone.blocks to backbone.layers
        if 'backbone.blocks' in key:
            new_key = key.replace('backbone.blocks', 'backbone.layers')
            new_key = new_key.replace('norm', 'ln')
            new_key = new_key.replace('mlp.fc1', 'ffn.layers.0.0')
            new_key = new_key.replace('mlp.fc2', 'ffn.layers.1')
            target_state_dict['state_dict'][new_key] = value
        # Convert final norm to ln1
        elif 'backbone.norm' in key:
            new_key = key.replace('backbone.norm', 'backbone.ln1')
            target_state_dict['state_dict'][new_key] = value
        # Convert patch_embed.proj to patch_embed.projection
        elif 'backbone.patch_embed.proj' in key:
            new_key = key.replace('backbone.patch_embed.proj', 'backbone.patch_embed.projection')
            target_state_dict['state_dict'][new_key] = value
        else:
            target_state_dict['state_dict'][key] = value
    torch.save(target_state_dict, output_pth_path)
    print(f"Filtered state_dict saved to {output_pth_path}")




    
# 假设您已经加载了预训练权重

# pretrained_weights = torch.load('vit-base-p14_dinov2-pre_3rdparty_20230426-ba246503.pth')
# # 移除权重中的'backbone.'前缀
# updated_weights = remove_prefix_from_state_dict(pretrained_weights['state_dict'])
# # print(updated_weights)
# torch.save(updated_weights, 'vit-base-p14_dinov2-pre_3rdparty_20230426-ba246503_new.pth')

# 查看pth文件中的key
# pretrained_weights = torch.load('/home/yaoteam/yaoteam/yyc/random_paste_work/dino模型文件转换/checkpoint0299.pth', map_location="cpu")
pretrained_weights = torch.load('/home/yaoteam/yaoteam/yyc/random_paste_work/dino模型文件转换/all_unlabeled_img0730_0_1_checkpoint800.pth', map_location="cpu")
# Print the keys of the state dict

# pretrained_weights2 = torch.load('/home/yaoteam/yaoteam/yyc/mmpretrain/deit-small_pt-4xb256_in1k_20220218-9425b9bb.pth', map_location="cpu")
# for key in pretrained_weights.keys():
#     print(key)
# print("{0:=^60}".format("mocov3_vitb300"))
# for key in pretrained_weights['state_dict'].keys():
#     print(key)
# print("{0:=^60}".format("deit-small_pt-4xb256_in1k_20220218-9425b9bb.pth"))
# # for key in pretrained_weights2.keys():
# #     print(key)
# for key in pretrained_weights2['state_dict'].keys():
#     print(key)

convert_torch_hub_to_MoCoV3(pretrained_weights,'backbone.','/home/yaoteam/yaoteam/yyc/random_paste_work/dino模型文件转换/dino_teacher_all_unlabeled_img0730_0_1_checkpoint800.pth')