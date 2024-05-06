import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pydensecrf.densecrf as dcrf
from pydensecrf.utils import unary_from_labels, create_pairwise_bilateral

import label_color
from label_color import colorize_mask

# 初始标签
# 指定图像路径
image_path = r"G:\DataSets\cityscapes\gtCoarse\gtCoarse\train\aachen\aachen_000000_000019_gtCoarse_labelIds.png"
image = np.array(Image.open(r'G:\DataSets\cityscapes\leftImg8bit\train\aachen\aachen_000000_000019_leftImg8bit.png'))

# 使用PIL库读取图像
image_pil = Image.open(image_path)
# 将图像转换为NumPy数组
labels = np.array(image_pil)

# 设置dCRF参数
dcrf_params = {
    'compat_spat': 10,
    'compat_col': 50,
    'theta_spat': 3,
    'theta_col': 80,
    'num_iter': 10,
    'pos_xy_std': 1,
    'pos_w': 3
}

print(image.shape)
print(image.shape[1])
# 创建一个dCRF对象
d = dcrf.DenseCRF2D(image.shape[1], image.shape[0], 2)

# 设置unary势能（将标签作为unary势能的一部分）
U = unary_from_labels(labels, 2, gt_prob=0.9, zero_unsure=False)
d.setUnaryEnergy(U)

# 添加双边势能（双边滤波器）
d.addPairwiseBilateral(**dcrf_params)

# 运行推理
Q = d.inference(10)

# 得到最终标签
map_soln = np.argmax(Q, axis=0).reshape((image.shape[0], image.shape[1]))

# 可视化结果
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.imshow(image[:, :, ::-1])
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(label, cmap='jet')
plt.title('Original Segmentation Label')

plt.subplot(1, 3, 3)
plt.imshow(map_soln, cmap='jet')
plt.title('Segmentation Label after dCRF')

plt.show()
