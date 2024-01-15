import os

import numpy as np
from PIL import Image
image_path = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/ADEChallengeData2016/annotations/training/ADE_train_00000006.png'
label_path = r'/home/lab611/dcr/new/pytorch-segmentation-master/output/ade20k/ADE_train_00000006.png'

pixel_number_list = [[0, 1472092, 622903, 1763976, 1031580, 1502058, 3496584, 2993896, 5785458, 1913799, 2282939, 2326733, 3352147, 2033111, 1861247, 10572105, 1457716, 1356007, 2534339, 3145856, 1779999], [0, 922858, 447056, 896897, 452163, 564205, 1512717, 1104240, 2555721, 1054701, 998591, 589700, 2300720, 516643, 1227650, 4786934, 595873, 1006317, 1368572, 1943506, 761368], [0, 288437, 177078, 585334, 206046, 282625, 1065801, 651087, 1154206, 513749, 493346, 833885, 919530, 435599, 363711, 2571711, 202096, 408690, 1071042, 463432, 571945], [0, 195226, 68697, 384194, 297367, 416101, 729731, 561007, 1118210, 477840, 375422, 852742, 630787, 495832, 560391, 2063346, 424134, 567921, 780818, 1210575, 583764]]

if __name__ == '__main__':

    for client in pixel_number_list:
        print(client)
    weight = [0.0]*4
    n = len(pixel_number_list)
    pixel_per_list = []
    for i in range(n):
        pixel_per_list.append([0.0])
    for i in range(1, 21):
        tot = 0.0
        for j in range(n):
            tot = tot + pixel_number_list[j][i]
        for j in range(n):
            pixel_per_list[j].append(pixel_number_list[j][i] / tot)
    for i in range(n):
        for j in range(1, 21):
            weight[i] = weight[i] + pixel_per_list[i][j] / 20
    print(pixel_per_list)
    print(weight)
    print(sum(weight))
    # image_1 = np.asarray(Image.open(image_path), dtype=np.int32)
    # image_2 = np.asarray(Image.open(label_path), dtype=np.int32)
    # print(image_2)
    # num = 0.0
    # acc = 0.0
    # for i in range(image_2.shape[0]):
    #     for j in range(image_2.shape[1]):
    #         num = num + 1
    #         if image_1[i][j] != 0 and image_1[i][j] == image_2[i][j]:
    #             print(image_2[i][j], end=' ')
    #             acc = acc + 1
    #     print('')
    # print(acc/num)