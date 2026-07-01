import os
import zipfile
from tqdm import tqdm

def compress_images_in_batches(input_folder, output_folder, batch_size=5000):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取输入文件夹中的所有图片文件
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    # 计算需要多少个批次
    total_files = len(image_files)
    num_batches = (total_files // batch_size) + (1 if total_files % batch_size != 0 else 0)
    
    for i in range(num_batches):
        batch_files = image_files[i * batch_size : (i + 1) * batch_size]
        zip_filename = os.path.join(output_folder, f'background_wait_check_batch_{i + 1}.zip')
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in tqdm(batch_files, desc=f'Compressing batch {i + 1}/{num_batches}', unit='file'):
                file_path = os.path.join(input_folder, file)
                zipf.write(file_path, arcname=file)
                
        print(f'Batch {i + 1} compressed to {zip_filename}')

# 示例用法
input_folder = r'/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯/分离出来的背景图及其标注文件'
output_folder = r'/home/yaoteam/yaoteam/yyc/YYC_SSD/高空测报灯'
compress_images_in_batches(input_folder, output_folder, batch_size=5000)
