import os

def get_image_filenames(folder, extensions={'.jpg', '.jpeg', '.png', '.bmp', '.gif'}):
    """
    获取指定文件夹中所有图片文件的文件名（不含路径）
    """
    return {f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in extensions}

def compare_image_filenames(folder1, folder2):
    files1 = get_image_filenames(folder1)
    files2 = get_image_filenames(folder2)

    common = files1 & files2  # 两个文件夹都有
    only_in_folder1 = files1 - files2
    only_in_folder2 = files2 - files1

    print(f"✅ 两个文件夹中共同的图片文件数: {len(common)}")
    for name in sorted(common):
        print(f"  ✓ {name}")

    print(f"\n❌ 仅在 {folder1} 中的图片文件数: {len(only_in_folder1)}")
    # for name in sorted(only_in_folder1):
    #     print(f"  - {name}")

    print(f"\n❌ 仅在 {folder2} 中的图片文件数: {len(only_in_folder2)}")
    # for name in sorted(only_in_folder2):
    #     print(f"  - {name}")

# 示例使用
folder1 = '/home/yaoteam/yaoteam/wz/测试/测试集/双斑痕叶蝉/'
folder2 = '/home/yaoteam/yaoteam/wz/飞虱叶蝉训练集_种/val/双斑痕叶蝉/'

compare_image_filenames(folder1, folder2)