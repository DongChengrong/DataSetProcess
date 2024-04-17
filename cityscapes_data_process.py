import os
import shutil
import label_color
import random

IN_PATH = r'G:\DataSets\cityscapes\leftImg8bit'
OUT_PATH = r'G:\DataSets\cityscapes\cityscapes_image'

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

def samples_select(IN_PATH, OUT_PATH):
    # 如果目标文件夹不存在，创建它
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    # 遍历所有的文件夹
    for file in os.listdir(IN_PATH):
        src_item = os.path.join(IN_PATH, file)

        if os.path.isdir(src_item):
            samples_select(src_item, OUT_PATH)
        else:
            # 检查文件结尾是否是instance
            if file.endswith(".png"):
                dst_item = os.path.join(OUT_PATH, file)
                print(dst_item)
                shutil.copy(src_item, dst_item)

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



def select_instance_labels(IN_PATH, OUT_PATH):
    # 如果目标文件夹不存在，创建它
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    # 遍历所有的文件夹
    for file in os.listdir(IN_PATH):
        src_item = os.path.join(IN_PATH, file)

        if os.path.isdir(src_item):
            select_instance_labels(src_item, OUT_PATH)
        else:
            # 检查文件结尾是否是instance
            if file.endswith("instanceIds.png"):
                dst_item = os.path.join(OUT_PATH, file)
                print(dst_item)
                shutil.copy(src_item, dst_item)


def select_semantic_labels(IN_PATH, OUT_PATH):
    # 如果目标文件夹不存在，创建它
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    # 遍历所有的文件夹
    for file in os.listdir(IN_PATH):
        src_item = os.path.join(IN_PATH, file)

        if os.path.isdir(src_item):
            select_semantic_labels(src_item, OUT_PATH)
        else:
            # 检查文件结尾是否是instance
            if file.endswith("_gtFine_instanceIds.png"):
                dst_item = os.path.join(OUT_PATH, file)
                print(dst_item)
                shutil.copy(src_item, dst_item)

if __name__ == '__main__':
    #samples_select(IN_PATH, OUT_PATH)
    in_path = r'G:\DataSets\fedMTL\cityscapes\split_2\client1\image'
    out_path = r'G:\DataSets\fedMTL\cityscapes\split_2\client3\image'
    move_random_images(in_path, out_path)