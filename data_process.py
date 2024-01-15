import os
import shutil
from PIL import Image

IMAGE_PATH = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/VOCdevkit/VOC2012/JPEGImages'
OUT_PATH = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/VOCdevkit/VOC2012/SegImage'
LABEL_PATH = r'G:\DataSets\PascalVOC\VOCdevkit\VOC2011\ImageSets\Segmentation\trainval.txt'
TXT_FILE_PATH = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/VOCdevkit/VOC2012/ImageSets/Segmentation/trainval.txt'

# 按照标签将有标签数据从无标签数据中摘出来
def select_labeled_data():
    with open(LABEL_PATH, 'r') as f:
        line = f.readline().strip()
        while line:
            id = str(line) + '.jpg'
            image_path = os.path.join(IMAGE_PATH, id)
            print(image_path)
            shutil.copy(image_path, OUT_PATH)
            line = f.readline().strip()

# 划分数据集

# 将一个目录下的所有文件全部复制到指定文件夹
def copy_to_dir(in_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for item in os.listdir(in_dir):
        src_item = os.path.join(in_dir, item)

        if os.path.isdir(src_item):
            copy_to_dir(src_item, out_dir)
        else:
            dst_item = os.path.join(out_dir, item)
            print(dst_item)
            shutil.copy(src_item, dst_item)

# 去除文件扩展名
def remove_extension(filename):
    return os.path.splitext(filename)[0]

# 将列表中的内容保存在一个txt文件中
def save_to_txt(file_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file in file_list:
            train_id = remove_extension(file) + '\n'
            print(train_id)
            f.write(train_id)

# 得到指定文件夹文件的id
def get_files_id(in_dir):
    file_list = [f for f in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir, f))]
    save_to_txt(file_list, TXT_FILE_PATH)

# 按照txt中的id将实例标签放入对应文件夹
def select_ins_labeled_data():
    with open(TXT_FILE_PATH, 'r') as f:
        line = f.readline().strip()
        while line:
            id = str(line) + '.jpg'
            image_path = os.path.join(IMAGE_PATH, id)
            print(image_path)
            shutil.copy(image_path, OUT_PATH)
            line = f.readline().strip()

if __name__ == '__main__':
    #select_labeled_data()
    #copy_to_dir(IMAGE_PATH, OUT_PATH)
    #get_files_id(OUT_PATH)
    select_ins_labeled_data()