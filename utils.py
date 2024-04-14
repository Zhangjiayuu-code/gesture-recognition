import os
import torch


def create_experiment_folder(base_dir="runs"):
    """
    create exp folder and return the exp_path
    """
    # 确保基目录存在
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # 查找已存在的实验文件夹并确定下一个编号
    existing_folders = [d for d in os.listdir(base_dir) if d.startswith('exp')]
    if existing_folders:
        # 获取已存在文件夹的编号
        numbers = [int(folder.replace('exp', '')) for folder in existing_folders if folder.replace('exp', '').isdigit()]
        # 确定下一个可用编号
        next_number = max(numbers) + 1
    else:
        # 如果没有找到文件夹，从1开始编号
        next_number = 1

    # 创建新的实验文件夹
    new_exp_name = f"exp{next_number}"
    new_exp_path = os.path.join(base_dir, new_exp_name)
    os.makedirs(new_exp_path, exist_ok=True)

    return new_exp_path

# 示例用法
if __name__=="__main__":
    new_exp_path = create_experiment_folder()
    print("New experiment folder created at:", new_exp_path)
