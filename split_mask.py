import numpy as np
from PIL import Image
from skimage import io
import matplotlib.pyplot as plt
from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage.segmentation import my_mark_boundaries
import sys
from palette import CityScpates_palette
from util import colorize_mask

save_dir = r'G:\github_codes\DataSetProcess'
ins_dict = {}  # 记录实例区域出现最多的伪标签是什么
ins_seg_match = {}  # 记录实例应该保存什么标签
save_path = r'G:\github_codes\DataSetProcess\tmp.png'


# 使用深度优先首先对图像块进行重新编号
def dfs(vis, boud, cnt, start_x, start_y, max_x, max_y):
    stack = [(start_x, start_y)]  # 用栈来模拟递归调用

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= max_x or y < 0 or y >= max_y or vis[x][y] != 0 or boud[x][y] == np.bool_(True):
            continue
        vis[x][y] = cnt
        for i in range(-1, 2):
            for j in range(-1, 2):
                stack.append((x + i, y + j))
            stack.append((x + i, y + j))


# 根据RGB值将实例映射为一个整数ID
def re_id(matrix):
    # print(matrix)
    return int(matrix)
#    return matrix[0] * (256 * 256) + matrix[1] `* 256 + matrix[2]


def solve(file_path, label_path):
    image = np.array(Image.open(file_path))
    label = np.array(Image.open(label_path))
    print(label.shape)
    max_x = image.shape[0]
    max_y = image.shape[1]

    # 读取图片并将其转化为浮点型
    temp_image = img_as_float(io.imread(file_path))
    numSegments = 300

    # 应用slic算法并获取分割结果
    segments = slic(temp_image, n_segments=numSegments, sigma=5)
    boud = my_mark_boundaries(image, segments)
    # 查看边界情况
    # for i in range(max_x):
    #     for j in range(max_y):
    #         if boud[i][j] == np.bool_(True):
    #             print(f'{i}     {j}')
    mask = np.zeros((max_x, max_y))  # 超像素掩码区域
    cnt = 1
    for i in range(0, max_x):
        for j in range(0, max_y):
            if mask[i][j] == 0 and boud[i][j] == np.bool_(False):
                dfs(mask, boud, cnt, i, j, max_x, max_y)
                cnt = cnt + 1

    ins_dict.clear()
    ins_seg_match.clear()
    copied_image = label.copy()
    h, w = image.shape[0], image.shape[1]
    # print(f'{image.shape}   {pseudo_label.shape}')
    for i in range(h):
        for j in range(w):
            ID = re_id(mask[i][j])  # 得到实例对应的唯一ID
            pse_label = label[i][j]  # 得到该像素对应的伪标签
            if ID not in ins_dict:  # 如果第一次出现该实例
                ins_dict[ID] = {}  # 该实例映射到一个字典
                ins_dict[ID][pse_label] = 1
            else:
                if pse_label not in ins_dict[ID]:  # 该实例中第一次出现该伪标签
                    ins_dict[ID][pse_label] = 1
                else:
                    ins_dict[ID][pse_label] = ins_dict[ID][pse_label] + 1
    # 将每一个实例映射到一个语义类别
    for key1 in ins_dict.keys():
        count = 0
        max_num = 0
        max_key = 0
        tmp_dict = ins_dict[key1]
        for key2 in ins_dict[key1].keys():
            count = count + tmp_dict[key2]
            if tmp_dict[key2] > max_num:
                max_num = tmp_dict[key2]
                max_key = key2
            ins_seg_match[key1] = max_key

    # 遍历，生成细化后的伪标签
    for i in range(h):
        for j in range(w):
            ID = re_id(mask[i][j])
            copied_image[i][j] = ins_seg_match[ID]

    new_mask = colorize_mask(copied_image, CityScpates_palette)
    new_mask.save(save_path)


if __name__ == '__main__':
    image_path = r'G:\DataSets\cityscapes\leftImg8bit\train\aachen\aachen_000000_000019_leftImg8bit.png'
    label_path = r'G:\DataSets\cityscapes\gtCoarse\gtCoarse\train\aachen\aachen_000000_000019_gtCoarse_labelIds.png'
    solve(image_path, label_path)
