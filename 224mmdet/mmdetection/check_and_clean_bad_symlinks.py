import os
import cv2
from PIL import Image
from tqdm import tqdm

# ========== 配置部分 ==========
ROOT_DIR = "/home/star/2T-new/wz/2024-2025年未审核测报灯图片软链接汇总"
BAD_LOG = "bad_symlinks.txt"
# =============================

def is_image_file(path):
    return path.lower().endswith((".jpg", ".jpeg", ".png"))

def check_image_valid(target_path):
    """检查图片文件是否有效（cv2 + Pillow 双重验证）"""
    if not os.path.exists(target_path):
        return False
    try:
        img = cv2.imread(target_path)
        if img is None:
            return False
    except Exception:
        return False

    try:
        with Image.open(target_path) as im:
            im.verify()
    except Exception:
        return False
    return True

def main():
    bad_links = []
    total = 0

    # 遍历所有文件
    for root, _, files in os.walk(ROOT_DIR):
        for name in files:
            if not is_image_file(name):
                continue
            total += 1
            path = os.path.join(root, name)
            if not os.path.islink(path):
                continue

            target = os.readlink(path)
            # 如果是相对路径，则转为绝对路径
            if not os.path.isabs(target):
                target = os.path.join(os.path.dirname(path), target)
                target = os.path.abspath(target)

            valid = check_image_valid(target)
            if not valid:
                bad_links.append(path)
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"删除失败：{path} ({e})")

    # 记录坏图日志
    with open(BAD_LOG, "w", encoding="utf-8") as f:
        for p in bad_links:
            f.write(p + "\n")

    print("\n==============================")
    print(f"扫描完成：共 {total} 张图片")
    print(f"删除坏软链接：{len(bad_links)} 个")
    print(f"坏图路径已保存至：{BAD_LOG}")
    print("==============================")

if __name__ == "__main__":
    main()
