import os
import shutil
import random
from pathlib import Path


def split_images(source_folder, destination_folders, split_ratio):
    # 获取源文件夹中的所有图片文件
    image_files = [f for f in os.listdir(source_folder) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 计算每个文件夹应该包含的图片数量
    num_images = len(image_files)
    images_per_folder = [int(split_ratio[_] * num_images) for _ in range(len(destination_folders) - 1)]
    images_per_folder.append(num_images - sum(images_per_folder))

    # 将图片文件列表随机打乱
    random.shuffle(image_files)

    # 创建目标文件夹（如果不存在）
    for folder in destination_folders:
        Path(folder).mkdir(parents=True, exist_ok=True)

    # 按照划分比例将图片复制到目标文件夹
    start_index = 0
    for i, folder in enumerate(destination_folders):
        end_index = start_index + images_per_folder[i]
        for file_name in image_files[start_index:end_index]:
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(folder, file_name)
            shutil.copy2(source_path, destination_path)
        start_index = end_index


if __name__ == "__main__":
    # 指定源文件夹和目标文件夹
    source_folder = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/VOCdevkit/VOC2012/SegImage'
    destination_folders = [f"/home/lab611/dcr/datasets/split_6/client{i + 1}/image" for i in range(6)]

    # 指定划分比例（每个文件夹的图片数量占总图片数量的比例）
    split_ratios = (0.3, 0.2, 0.1, 0.1, 0.1, 0.2)

    # 执行划分操作
    split_images(source_folder, destination_folders, split_ratios)
