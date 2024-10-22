import os
import os
import shutil
import zipfile

def clear_target_folder(target_dir):
    # 如果目标文件夹存在，删除它并重新创建
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

def copy_log_files(source_dir, target_dir, log_filename="hacpp.log"):
    # 遍历源目录
    for root, dirs, files in os.walk(source_dir):
        # 检查是否有匹配的log文件
        if log_filename in files:
            # 计算源文件的完整路径
            source_file_path = os.path.join(root, log_filename)
            
            # 计算相对于源目录的路径，并构造目标路径
            relative_path = os.path.relpath(root, source_dir)
            target_subdir = os.path.join(target_dir, relative_path)
            
            # 创建目标子目录
            os.makedirs(target_subdir, exist_ok=True)
            
            # 构造目标文件的完整路径
            target_file_path = os.path.join(target_subdir, log_filename)
            
            # 复制文件
            shutil.copy2(source_file_path, target_file_path)
            print(f"Copied {source_file_path} to {target_file_path}")

def zip_folder(target_dir, zip_file_path):
    # 压缩目标文件夹为zip文件
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历目标文件夹，递归添加文件到zip
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 计算相对于目标文件夹的路径
                relative_path = os.path.relpath(file_path, target_dir)
                zipf.write(file_path, relative_path)
    print(f"Zipped {target_dir} to {zip_file_path}")

# 示例使用
source_folder = "/root/autodl-tmp/HAC_ES/outputs"  # 替换为你的源文件夹路径
target_folder = "/root/autodl-tmp/HAC_ES/collect_output"  # 替换为你的目标文件夹路径
zip_file = "/root/autodl-tmp/HAC_ES/target_folder.zip"   # 替换为压缩后的zip文件路径

# 清空目标文件夹
clear_target_folder(target_folder)

# 复制文件
copy_log_files(source_folder, target_folder)

# 压缩目标文件夹
zip_folder(target_folder, zip_file)
# 示例使用


