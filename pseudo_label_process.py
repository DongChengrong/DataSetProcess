import os
import shutil
import numpy as np
from PIL import Image


IMAGE_PATH = r'G:\DataSets\ADE20K\ADE20K-instance\annotations_instance\training'
OUT_PATH = r'G:\DataSets\ADE20K\ADE20K_all\ins_label'
INS_LABEL_PATH = r'G:\DataSets\ADE20K\ADE20K_all\ins_label'
LABEL_PATH = r'G:\DataSets\PascalVOC\VOCdevkit\VOC2011\ImageSets\Segmentation\trainval.txt'
TXT_FILE_PATH = r'G:\DataSets\ADE20K\ADE20K_all\train.txt'

# 读取实例分割的标签
def read_ins_label():
    file_list = [os.path.join(INS_LABEL_PATH, f) for f in os.listdir(INS_LABEL_PATH) if os.path.isfile(os.path.join(INS_LABEL_PATH, f))]
    for file in file_list:
        print(file)
        image = Image.open(file)
        image_data = np.array(image)
        print(image_data)
        exit(0)

if __name__ == '__main__':
    read_ins_label()