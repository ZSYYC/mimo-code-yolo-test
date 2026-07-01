import os
import argparse
from PIL import Image
from pathlib import Path

def bmp_to_jpg(input_dir, quality=95, overwrite=False):
    """
    将指定目录下的所有BMP图片转换为JPG格式
    
    参数:
        input_dir: 包含BMP文件的文件夹路径
        quality: JPG质量 (1-95，默认95)
        overwrite: 是否覆盖已存在的JPG文件 (默认False)
    """
    # 验证输入目录是否存在
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"错误：目录 '{input_dir}' 不存在！")
        return
    
    if not input_path.is_dir():
        print(f"错误：'{input_dir}' 不是有效的文件夹！")
        return
    
    # 获取所有BMP文件
    bmp_files = list(input_path.glob("*.bmp")) + list(input_path.glob("*.BMP"))
    
    if not bmp_files:
        print(f"在目录 '{input_dir}' 中未找到任何BMP文件")
        return
    
    print(f"找到 {len(bmp_files)} 个BMP文件，开始转换...\n")
    
    success_count = 0
    fail_count = 0
    
    for idx, bmp_file in enumerate(bmp_files, 1):
        # 构建输出文件名
        jpg_filename = bmp_file.stem + ".jpg"
        jpg_filepath = bmp_file.parent / jpg_filename
        
        # 检查是否已存在且不覆盖
        if jpg_filepath.exists() and not overwrite:
            print(f"[{idx}/{len(bmp_files)}] 跳过 {bmp_file.name} - {jpg_filename} 已存在")
            continue
        
        try:
            # 打开BMP文件并转换为JPG
            with Image.open(bmp_file) as img:
                # 处理RGBA格式（JPG不支持透明通道）
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # 保存为JPG
                img.save(jpg_filepath, 'JPEG', quality=quality, optimize=True)
            
            print(f"[{idx}/{len(bmp_files)}] 成功：{bmp_file.name} -> {jpg_filename}")
            success_count += 1
        
        except Exception as e:
            print(f"[{idx}/{len(bmp_files)}] 失败：{bmp_file.name} - 错误：{str(e)}")
            fail_count += 1
    
    # 输出转换总结
    print(f"\n转换完成！")
    print(f"成功：{success_count} 个文件")
    print(f"失败：{fail_count} 个文件")
    print(f"跳过：{len(bmp_files) - success_count - fail_count} 个文件")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='批量将指定文件夹中的BMP图片转换为JPG格式')
    parser.add_argument('directory', help='包含BMP文件的文件夹路径')
    parser.add_argument('-q', '--quality', type=int, default=95, 
                        help='JPG图片质量 (1-95，默认95)')
    parser.add_argument('-o', '--overwrite', action='store_true', 
                        help='覆盖已存在的JPG文件 (默认不覆盖)')
    
    args = parser.parse_args()
    
    # 执行转换
    bmp_to_jpg(args.directory, args.quality, args.overwrite)

if __name__ == "__main__":
    # 先检查PIL库是否安装
    try:
        from PIL import Image
    except ImportError:
        print("错误：未安装Pillow库，请先执行以下命令安装：")
        print("pip install pillow")
        exit(1)
    
    main()