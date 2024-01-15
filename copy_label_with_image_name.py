import os
import shutil
from pathlib import Path

# image_dir = r'/home/lab611/dcr/datasets/split_2/val/image'
pseudo_label_dir = r'/home/lab611/dcr/new/pytorch-segmentation-master/fine_label/voc2012'
label_dir = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/VOCdevkit/VOC2012/SegmentationClass'


# output_dir = r'/home/lab611/dcr/datasets/split_2/val/label'

def copy_files_with_different_extension(folder1, folder2, folder3):
    # 获取第一个文件夹中的所有文件名（不包括扩展名）
    filenames_folder1 = {os.path.splitext(file)[0] for file in os.listdir(folder1)}

    # 确保第三个文件夹存在，如果不存在则创建
    if not os.path.exists(folder3):
        os.makedirs(folder3)

    # 遍历第二个文件夹中的文件
    for filename in os.listdir(folder2):
        # 分离文件名和扩展名
        name, extension = os.path.splitext(filename)

        # 如果文件名在第一个文件夹中存在，且扩展名不同，则进行复制
        if name in filenames_folder1 and extension != "":
            source_path = os.path.join(folder2, filename)
            destination_path = os.path.join(folder3, filename)

            # 使用shutil.copyfile进行文件复制
            shutil.copyfile(source_path, destination_path)
            print(f"File '{filename}' copied to {folder3}")


if __name__ == '__main__':
    image_dir = [f"/home/lab611/dcr/datasets/split_6/client{i + 1}/image" for i in range(6)]

    output_dir = [f"/home/lab611/dcr/datasets/split_6/client{i + 1}/label" for i in range(6)]
    for folder in output_dir:
        Path(folder).mkdir(parents=True, exist_ok=True)
    for i in range(5,6):
        copy_files_with_different_extension(image_dir[i], label_dir, output_dir[i])
