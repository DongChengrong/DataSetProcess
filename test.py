import numpy as np
from PIL import Image


def ID(matrix):
    # return matrix
    return matrix[0] * (256 * 256) + matrix[1] * 256 + matrix[2]


# 读取图像文件  
image_path = 'G:\DataSets/cityscapes/cityscapes_instance/aachen_000016_000019_gtFine_instanceIds.png'  # 替换为你的图像文件路径
image = Image.open(image_path)

# 确保图像是RGB格式  
if image.mode != 'RGB':
    image = image.convert('RGB')

# 获取图像的宽和高  
width = np.array(image).shape[0]
height = np.array(image).shape[1]
myDict = {}
color_count = 0
colors = [[241, 215, 126], [147, 75, 67], [147, 148, 231], [215, 99, 100], [177, 206, 70], [95, 151, 210]]

image = np.array(image)

for y in range(height):
    for x in range(width):
        # 获取像素的RGB值
        r, g, b = image[x][y][0], image[x][y][1], image[x][y][2]
        if x == 300:
            print(f'{r}  {g}  {b}')
        if r == 11 and g == 11 and b == 11:
            continue
        iid = ID(image[x, y])
        if iid in myDict:
            image[x][y] = colors[myDict[iid]]
        else:
            myDict[iid] = color_count
            color_count = color_count + 1
            image[x][y] = colors[myDict[iid]]
            if color_count == 6:
                color_count = 0

image = Image.fromarray(image)
image.save('G:\DataSets/cityscapes/visualization_results/with_ins/aachen_000016_000019_gtFine_instanceIds.png')
