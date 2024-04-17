import os
import shutil
import random
from pathlib import Path

import numpy as np
from PIL import Image

# 指定源文件夹和目标文件夹
client_image_dir = [f"G:\DataSets/fedMTL/cityscapes/split_2/client{i + 1}/image" for i in range(6)]
client_label_dir = [f"G:\DataSets/fedMTL/cityscapes/split_2/client{i + 1}/label" for i in range(6)]
pan_path = r'G:\FedMTL实验数据\fine_labels\cityscapes\method3\with_pan'
image_dir = r'G:\DataSets\cityscapes\cityscapes_image'
ins_dir = r'G:\FedMTL实验数据\fine_labels\cityscapes\method3\with_ins'
seg_dir = r'G:\DataSets\cityscapes\cityscapes_sem_trainid'

def split_images(source_folder, destination_folders, split_ratio):
    # 获取源文件夹中的所有图片文件
    pan_files = set(os.listdir(pan_path))
    image_files = set(os.listdir(image_dir))

    image_files = list(image_files - pan_files)

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
        if i == 3 or i == 4:
            continue
        end_index = start_index + images_per_folder[i]
        for file_name in image_files[start_index:end_index]:
            source_path = os.path.join(source_folder, file_name)
            destination_path = os.path.join(folder, file_name)
            print(destination_path)
            shutil.copy2(source_path, destination_path)
        start_index = end_index

def pan_split(split_ratios):
    num = 3475
    client1_num = int(num * split_ratios[3])
    client2_num = int(num * split_ratios[4])

    dst_1 = r'G:\DataSets\fedMTL\cityscapes\split_1\client4\label'
    dst_2 = r'G:\DataSets\fedMTL\cityscapes\split_1\client5\label'


    image_files = [f for f in os.listdir(pan_path) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    random.shuffle(image_files)

    for file_name in image_files[0:client1_num]:
        source_path = os.path.join(pan_path, file_name)
        destination_path = os.path.join(dst_1, file_name)
        print(destination_path)
        shutil.copy2(source_path, destination_path)

    for file_name in image_files[1500:1500+client2_num]:
        source_path = os.path.join(pan_path, file_name)
        destination_path = os.path.join(dst_2, file_name)
        print(destination_path)
        shutil.copy2(source_path, destination_path)

def move_random_images(source_folder, destination_folder):
    # 获取源文件夹中的所有图像文件
    image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 计算要移动的图像数量（1/3）
    num_images_to_move = len(image_files) // 3

    # 随机选择要移动的图像
    images_to_move = random.sample(image_files, num_images_to_move)

    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 移动图像到目标文件夹
    for image in images_to_move:
        source_path = os.path.join(source_folder, image)
        destination_path = os.path.join(destination_folder, image)
        shutil.move(source_path, destination_path)
        print(f"Moved: {image}")

def copy_by_label(folder1, folder2, folder3):
    # 获取第一个文件夹中的所有文件名（不包括扩展名）
    filenames_folder1 = [f for f in os.listdir(folder1) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 确保第三个文件夹存在，如果不存在则创建
    if not os.path.exists(folder3):
        os.makedirs(folder3)

    # 遍历第二个文件夹中的文件
    for filename in filenames_folder1:
        # 分离文件名和扩展名
        name = filename.replace('_leftImg8bit', '_gtFine_labelIds')

        source_path = os.path.join(folder2, name)

        # 如果文件名在第一个文件夹中存在，且扩展名不同，则进行复制
        destination_path = os.path.join(folder3, name.replace('_leftImg8bit','_gtFine_labelIds'))

        # 使用shutil.copyfile进行文件复制
        shutil.copyfile(source_path, destination_path)
        print(f"File '{filename}' copied to {destination_path}")

def copy_by_image(folder1, folder2, folder3):
    # 获取第一个文件夹中的所有文件名（不包括扩展名）
    filenames_folder1 = [f for f in os.listdir(folder1) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 确保第三个文件夹存在，如果不存在则创建
    if not os.path.exists(folder3):
        os.makedirs(folder3)

    # 遍历第二个文件夹中的文件
    for filename in filenames_folder1:
        # 分离文件名和扩展名
        name = filename.replace('_leftImg8bit', '_gtFine_labelIds')

        source_path = os.path.join(folder2, name)

        # 如果文件名在第一个文件夹中存在，且扩展名不同，则进行复制
        destination_path = os.path.join(folder3, name)

        # 使用shutil.copyfile进行文件复制
        shutil.copyfile(source_path, destination_path)
        print(f"File '{filename}' copied to {destination_path}")

def re_id(id1, id2):
    return id1 * 100 + id2

def decode(id):
    return id / 100, id %100

if __name__ == "__main__":

    # 指定划分比例（每个文件夹的图片数量占总图片数量的比例）
    split_ratios = (0.3, 0.2, 0.1, 0.1, 0.1, 0.2)
    # pan_split(split_ratios)
    # filenames_folder1 = [f for f in os.listdir(seg_dir) if
    #                      f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    # for i in range(3,5):
    #     copy_by_label(client_label_dir[i], image_dir, client_image_dir[i])
    # 执行划分操作
    # split_images(image_dir, client_image_dir, split_ratios)

    for i in range(6):
        if i != 2:
            continue
        copy_by_label(client_image_dir[i], ins_dir, client_label_dir[i])
