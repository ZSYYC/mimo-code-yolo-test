import os

def get_filenames_without_extension(folder):
    """Get a set of filenames without extensions from the given folder."""
    return {os.path.splitext(filename)[0] for filename in os.listdir(folder) if os.path.isfile(os.path.join(folder, filename))}

def find_duplicate_filenames(main_folder, other_folders):
    """Find and list duplicate filenames (without extension) across multiple folders."""
    main_filenames = get_filenames_without_extension(main_folder)
    
    all_other_filenames = set()
    for folder in other_folders:
        all_other_filenames.update(get_filenames_without_extension(folder))
    
    duplicates = main_filenames.intersection(all_other_filenames)
    return duplicates

# Example usage
main_folder = "/home/yaoteam/yaoteam/yyc/mmdet_dino/新整理的测报灯网站以及水稻所拍摄混合虫样图0724/水稻所拍摄"
other_folders = [
    "/home/yaoteam/yaoteam/yyc/mmdet_dino/所有图片VOC汇总_81955",
    "/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images",
    # "/home/yaoteam/yaoteam/yyc/mmdet_dino/folder3"
]

duplicates = find_duplicate_filenames(main_folder, other_folders)

if duplicates:
    print("Duplicate filenames found:")
    for filename in duplicates:
        print(filename)
else:
    print("No duplicate filenames found.")
