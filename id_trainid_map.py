import os

import numpy as np
from PIL import Image
import label_color

client1_path = r'G:\DataSets\cityscapes\cityscapes_semantic'
val_path = r'G:\DataSets\fedMTL\cityscapes\split_1\val\label'
gt_path = r'G:\DataSets\cityscapes\cityscapes_sem'
out_path = r'G:\DataSets\cityscapes\cityscapes_sem_trainid'

ignore_label = 255
ID_TO_TRAINID = {-1: ignore_label, 0: ignore_label, 1: ignore_label, 2: ignore_label,
                    3: ignore_label, 4: ignore_label, 5: ignore_label, 6: ignore_label,
                    7: 0, 8: 1, 9: ignore_label, 10: ignore_label, 11: 2, 12: 3, 13: 4,
                    14: ignore_label, 15: ignore_label, 16: ignore_label, 17: 5,
                    18: ignore_label, 19: 6, 20: 7, 21: 8, 22: 9, 23: 10, 24: 11, 25: 12, 26: 13, 27: 14,
                    28: 15, 29: ignore_label, 30: ignore_label, 31: 16, 32: 17, 33: 18}

if __name__ == '__main__':

    # count = 0
    file_list = os.listdir(client1_path)
    # label = np.asarray(Image.open(os.path.join(gt_path, filename)), dtype=np.int32)
    # label = label.copy()
    #
    # for i in range(label.shape[0]):
    #     for j in range(label.shape[1]):
    #         if label[i][j] == 26:
    #             count = count + 1
    # print(count)
    #
    # for k, v in ID_TO_TRAINID.items():
    #     label[label == k] = v
    #
    # count = 0
    # for i in range(label.shape[0]):
    #     for j in range(label.shape[1]):
    #         if label[i][j] == 26:
    #             count = count + 1
    # print(count)

    for filename in file_list:
        label_path = os.path.join(client1_path, filename)

        # 检查文件是否是一个图像文件（这里假设只处理常见的图像文件格式，如 JPEG、PNG）
        # 打开图像文件
        label = np.asarray(Image.open(label_path), dtype=np.int32)
        label = label.copy()
        # 在这里可以对图像进行任何你需要的处理

        for k, v in ID_TO_TRAINID.items():
            label[label == k] = v

        label_color.save_images(Image.open(label_path), label, out_path, filename, label_color.CityScpates_palette)