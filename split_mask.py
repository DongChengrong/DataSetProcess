import numpy as np
from PIL import Image
from skimage import io
import matplotlib.pyplot as plt
from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage.segmentation import my_mark_boundaries
import sys

# 使用深度优先首先对图像块进行重新编号
def dfs(vis, boud, cnt, start_x, start_y, max_x, max_y):
    stack = [(start_x, start_y)]  # 用栈来模拟递归调用

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= max_x or y < 0 or y >= max_y or vis[x][y] != 0 or boud[x][y] == np.bool_(True):
            continue

        vis[x][y] = cnt
        print(f'{x}   {y}       {vis[x][y]}')

        for i in range(-1, 2):
            for j in range(-1, 2):
                stack.append((x + i, y + j))
            stack.append((x + i, y + j))

def solve(file_path):
    image = np.array(Image.open(file_path))
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
    vis = np.zeros((max_x, max_y))
    cnt = 1
    for i in range(0, max_x):
        for j in range(0, max_y):
            if vis[i][j] == 0 and boud[i][j] == np.bool_(False):
                dfs(vis, boud, cnt, i, j, max_x, max_y)
                cnt = cnt + 1
    print(vis)

if __name__ == '__main__':
    solve(r'G:\DataSets\cityscapes\leftImg8bit\train\aachen\aachen_000000_000019_leftImg8bit.png')