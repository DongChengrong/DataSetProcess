import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from PIL import Image
import numpy as np

import label_color
from label_color import colorize_mask

# 定义随机游走函数
def random_walk(image, iterations=10, p=0.5):
    kernel = np.array([[0, p, 0],
                       [p, 0, p],
                       [0, p, 0]])
    result = np.copy(image)
    for _ in range(iterations):
        result = convolve(result, kernel, mode='constant', cval=0)
        result[result > 0] = 1
    return result


# 初始标签
# 指定图像路径
image_path = r"G:\DataSets\cityscapes\gtCoarse\gtCoarse\train\aachen\aachen_000000_000019_gtCoarse_labelIds.png"
# 使用PIL库读取图像
image_pil = Image.open(image_path)
# 将图像转换为NumPy数组
labels = np.array(image_pil)

# 通过随机游走传播标签
result = random_walk(labels, iterations=500, p=0.5)

labels = colorize_mask(labels, label_color.CityScpates_palette)
result = colorize_mask(result, label_color.CityScpates_palette)

# 绘制结果
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(labels, cmap='jet', vmin=0, vmax=1)
plt.title('Initial Labels')

plt.subplot(1, 3, 3)
plt.imshow(result, cmap='jet', vmin=0, vmax=1)
plt.title('Labels after Random Walk')

plt.show()
