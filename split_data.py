'''
在这份代码中实现了将数据集随机划分成两份并复制到不同的文件夹中
'''
import os
import random
import shutil

in_dir = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/VOCdevkit/VOC2012/SegImage'

out_dir_1 = r'/home/lab611/dcr/datasets/split_2/client1/image'
out_dir_2 = r'/home/lab611/dcr/datasets/split_2/client2/image'
out_dir_3 = r'/home/lab611/dcr/datasets/split_2/val/image'


def split_and_copy_images(source_folder, dest_folder1, dest_folder2, dest_folder3, split_ratios=(0.4, 0.4, 0.2)):
    # 获取源文件夹中的所有图片文件
    image_files = [f for f in os.listdir(source_folder) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 打乱图片文件顺序
    random.shuffle(image_files)

    # 计算每个部分的数量
    total_images = len(image_files)
    num_train = int(total_images * split_ratios[0])
    num_val = int(total_images * split_ratios[1])

    # 划分图片并拷贝到不同的目标文件夹
    train_images = image_files[:num_train]
    val_images = image_files[num_train:num_train + num_val]
    test_images = image_files[num_train + num_val:]

    for image in train_images:
        shutil.copy(os.path.join(source_folder, image), os.path.join(dest_folder1, image))

    for image in val_images:
        shutil.copy(os.path.join(source_folder, image), os.path.join(dest_folder2, image))

    for image in test_images:
        shutil.copy(os.path.join(source_folder, image), os.path.join(dest_folder3, image))


# 将数据集划分为两部分
def split_files(folder_path, split_ratio=0.5):
    # 获取文件夹中所有文件的路径
    all_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, file))]

    # 获取划分的索引
    total_files = len(all_files)
    split_index = int(total_files * split_ratio)

    # 随机打乱文件列表
    random.shuffle(all_files)

    # 划分文件列表
    train_files = all_files[:split_index]
    test_files = all_files[split_index:]

    return train_files, test_files


if __name__ == '__main__':
    # train_files, test_files = split_files(in_dir)
    #
    # print(f'Training files:{len(train_files)}张图片')
    # # print(train_files)
    #
    # print(f"\nTesting files:{len(test_files)}张图片")
    # # print(test_files)
    #
    # for file in train_files:
    #     shutil.copy(file, out_dir_1)
    # for file in test_files:
    #     shutil.copy(file, out_dir_2)
    split_and_copy_images(in_dir, out_dir_1, out_dir_2, out_dir_3)
