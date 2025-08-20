# 复制文本的链接到指定目录

import os
import shutil

# 设置源文件夹路径和目标文件夹路径
source_folder = r'g:\Submit\2025\2025年7月\ShareGPT-4o-Image_T2I_1597_20250704\image'
target_folder = r'g:\Submit\2025\2025年7月\ShareGPT-4o-Image_T2I_1597_20250704\err'

# 设置 .txt 文件路径
txt_file_path = r'g:\Submit\2025\2025年7月\ShareGPT-4o-Image_T2I_1597_20250704\62.txt'

# 读取txt文件，获取文件名列表
with open(txt_file_path, 'r', encoding='utf-8') as file:
    file_names = [line.strip() for line in file.readlines()]

# 遍历源文件夹的所有文件及子文件夹
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # 判断文件名是否在txt文件中
        if any(name in file for name in file_names):
            # 构造源文件的绝对路径
            src_file_path = os.path.join(root, file)
            # 构造目标文件的路径，保持文件夹结构
            relative_path = os.path.relpath(root, source_folder)
            target_dir = os.path.join(target_folder, relative_path)
            os.makedirs(target_dir, exist_ok=True)  # 确保目标文件夹存在
            target_file_path = os.path.join(target_dir, file)
            
            # 复制文件到目标路径
            shutil.copy2(src_file_path, target_file_path)
            print(f"文件 {file} 复制到 {target_file_path}")
