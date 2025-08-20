# 导出文件目录

import os

def export_file_list(root_dir, output_txt):
    """
    遍历 root_dir 及其所有子目录，将每个文件的完整路径写入 output_txt。
    """
    with open(output_txt, 'w', encoding='utf-8') as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                f.write(full_path + '\n')

if __name__ == '__main__':
    # TODO: 将下面的路径替换成你要扫描的文件夹和输出文件路径
    root_directory = r'G:\Submit\2025\2025年8月\第三轮鉴伪自测_1760_20250820'
    output_file = r'G:\Submit\2025\2025年8月\第三轮鉴伪自测_1760_20250820\4098.txt'
    export_file_list(root_directory, output_file)
    print(f'已将文件列表导出到：{output_file}')
