import numpy as np
from PIL import Image
import os
import multiprocessing as mp

from matplotlib import pyplot as plt

ALPHA = 0.3
highlight_object = [5,6,7,11,12,17,18]
weaker_object = [0, 2]
beta = 3.9
gamma = 0.7

ins_label_dir = r'/home/lab611/dcr/new/pytorch-segmentation-master/data/cityscapes_panotic/cityscapes_panoptic'
pseudo_label_dir = r'/home/lab611/dcr/new/pytorch-segmentation-master/output/cityscapes'
panoptic = r''

save_dir = r'/home/lab611/dcr/new/pytorch-segmentation-master/fine_label/cityscapes/method3/with_pan_2'
ins_dict = {}  # 记录实例区域出现最多的伪标签是什么
ins_seg_match = {}  # 记录实例应该保存什么标签

voc_palette = [0, 0, 0, 128, 0, 0, 0, 128, 0, 128, 128, 0, 0, 0, 128, 128, 0, 128, 0,
               128, 128, 128, 128, 128, 64, 0, 0, 192, 0, 0, 64, 128, 0, 192, 128, 0,
               64, 0, 128, 192, 0, 128, 64, 128, 128, 192, 128, 128, 0, 64, 0, 128, 64,
               0, 0, 192, 0, 128, 192, 0, 0, 64, 128]

ADE20K_palette = [0, 0, 0, 120, 120, 120, 180, 120, 120, 6, 230, 230, 80, 50, 50, 4, 200,
                  3, 120, 120, 80, 140, 140, 140, 204, 5, 255, 230, 230, 230, 4, 250, 7, 224,
                  5, 255, 235, 255, 7, 150, 5, 61, 120, 120, 70, 8, 255, 51, 255, 6, 82, 143,
                  255, 140, 204, 255, 4, 255, 51, 7, 204, 70, 3, 0, 102, 200, 61, 230, 250, 255,
                  6, 51, 11, 102, 255, 255, 7, 71, 255, 9, 224, 9, 7, 230, 220, 220, 220, 255, 9,
                  92, 112, 9, 255, 8, 255, 214, 7, 255, 224, 255, 184, 6, 10, 255, 71, 255, 41,
                  10, 7, 255, 255, 224, 255, 8, 102, 8, 255, 255, 61, 6, 255, 194, 7, 255, 122, 8,
                  0, 255, 20, 255, 8, 41, 255, 5, 153, 6, 51, 255, 235, 12, 255, 160, 150, 20, 0,
                  163, 255, 140, 140, 140, 250, 10, 15, 20, 255, 0, 31, 255, 0, 255, 31, 0, 255, 224
    , 0, 153, 255, 0, 0, 0, 255, 255, 71, 0, 0, 235, 255, 0, 173, 255, 31, 0, 255, 11, 200,
                  200, 255, 82, 0, 0, 255, 245, 0, 61, 255, 0, 255, 112, 0, 255, 133, 255, 0, 0, 255,
                  163, 0, 255, 102, 0, 194, 255, 0, 0, 143, 255, 51, 255, 0, 0, 82, 255, 0, 255, 41, 0,
                  255, 173, 10, 0, 255, 173, 255, 0, 0, 255, 153, 255, 92, 0, 255, 0, 255, 255, 0, 245,
                  255, 0, 102, 255, 173, 0, 255, 0, 20, 255, 184, 184, 0, 31, 255, 0, 255, 61, 0, 71, 255,
                  255, 0, 204, 0, 255, 194, 0, 255, 82, 0, 10, 255, 0, 112, 255, 51, 0, 255, 0, 194, 255, 0,
                  122, 255, 0, 255, 163, 255, 153, 0, 0, 255, 10, 255, 112, 0, 143, 255, 0, 82, 0, 255, 163,
                  255, 0, 255, 235, 0, 8, 184, 170, 133, 0, 255, 0, 255, 92, 184, 0, 255, 255, 0, 31, 0, 184,
                  255, 0, 214, 255, 255, 0, 112, 92, 255, 0, 0, 224, 255, 112, 224, 255, 70, 184, 160, 163,
                  0, 255, 153, 0, 255, 71, 255, 0, 255, 0, 163, 255, 204, 0, 255, 0, 143, 0, 255, 235, 133, 255,
                  0, 255, 0, 235, 245, 0, 255, 255, 0, 122, 255, 245, 0, 10, 190, 212, 214, 255, 0, 0, 204, 255,
                  20, 0, 255, 255, 255, 0, 0, 153, 255, 0, 41, 255, 0, 255, 204, 41, 0, 255, 41, 255, 0, 173, 0,
                  255, 0, 245, 255, 71, 0, 255, 122, 0, 255, 0, 255, 184, 0, 92, 255, 184, 255, 0, 0, 133, 255,
                  255, 214, 0, 25, 194, 194, 102, 255, 0, 92, 0, 255]

CityScpates_palette = [128, 64, 128, 244, 35, 232, 70, 70, 70, 102, 102, 156, 190, 153, 153, 153, 153, 153,
                       250, 170, 30, 220, 220, 0, 107, 142, 35, 152, 251, 152, 70, 130, 180, 220, 20, 60, 255, 0, 0, 0,
                       0, 142,
                       0, 0, 70, 0, 60, 100, 0, 80, 100, 0, 0, 230, 119, 11, 32, 128, 192, 0, 0, 64, 128, 128, 64, 128,
                       0, 192,
                       128, 128, 192, 128, 64, 64, 0, 192, 64, 0, 64, 192, 0, 192, 192, 0, 64, 64, 128, 192, 64, 128,
                       64, 192,
                       128, 192, 192, 128, 0, 0, 64, 128, 0, 64, 0, 128, 64, 128, 128, 64, 0, 0, 192, 128, 0, 192, 0,
                       128, 192,
                       128, 128, 192, 64, 0, 64, 192, 0, 64, 64, 128, 64, 192, 128, 64, 64, 0, 192, 192, 0, 192, 64,
                       128, 192,
                       192, 128, 192, 0, 64, 64, 128, 64, 64, 0, 192, 64, 128, 192, 64, 0, 64, 192, 128, 64, 192, 0,
                       192, 192,
                       128, 192, 192, 64, 64, 64, 192, 64, 64, 64, 192, 64, 192, 192, 64, 64, 64, 192, 192, 64, 192, 64,
                       192,
                       192, 192, 192, 192, 32, 0, 0, 160, 0, 0, 32, 128, 0, 160, 128, 0, 32, 0, 128, 160, 0, 128, 32,
                       128, 128,
                       160, 128, 128, 96, 0, 0, 224, 0, 0, 96, 128, 0, 224, 128, 0, 96, 0, 128, 224, 0, 128, 96, 128,
                       128, 224,
                       128, 128, 32, 64, 0, 160, 64, 0, 32, 192, 0, 160, 192, 0, 32, 64, 128, 160, 64, 128, 32, 192,
                       128, 160,
                       192, 128, 96, 64, 0, 224, 64, 0, 96, 192, 0, 224, 192, 0, 96, 64, 128, 224, 64, 128, 96, 192,
                       128, 224,
                       192, 128, 32, 0, 64, 160, 0, 64, 32, 128, 64, 160, 128, 64, 32, 0, 192, 160, 0, 192, 32, 128,
                       192, 160,
                       128, 192, 96, 0, 64, 224, 0, 64, 96, 128, 64, 224, 128, 64, 96, 0, 192, 224, 0, 192, 96, 128,
                       192, 224,
                       128, 192, 32, 64, 64, 160, 64, 64, 32, 192, 64, 160, 192, 64, 32, 64, 192, 160, 64, 192, 32, 192,
                       192,
                       160, 192, 192, 96, 64, 64, 224, 64, 64, 96, 192, 64, 224, 192, 64, 96, 64, 192, 224, 64, 192, 96,
                       192,
                       192, 224, 192, 192, 0, 32, 0, 128, 32, 0, 0, 160, 0, 128, 160, 0, 0, 32, 128, 128, 32, 128, 0,
                       160, 128,
                       128, 160, 128, 64, 32, 0, 192, 32, 0, 64, 160, 0, 192, 160, 0, 64, 32, 128, 192, 32, 128, 64,
                       160, 128,
                       192, 160, 128, 0, 96, 0, 128, 96, 0, 0, 224, 0, 128, 224, 0, 0, 96, 128, 128, 96, 128, 0, 224,
                       128, 128,
                       224, 128, 64, 96, 0, 192, 96, 0, 64, 224, 0, 192, 224, 0, 64, 96, 128, 192, 96, 128, 64, 224,
                       128, 192,
                       224, 128, 0, 32, 64, 128, 32, 64, 0, 160, 64, 128, 160, 64, 0, 32, 192, 128, 32, 192, 0, 160,
                       192, 128,
                       160, 192, 64, 32, 64, 192, 32, 64, 64, 160, 64, 192, 160, 64, 64, 32, 192, 192, 32, 192, 64, 160,
                       192,
                       192, 160, 192, 0, 96, 64, 128, 96, 64, 0, 224, 64, 128, 224, 64, 0, 96, 192, 128, 96, 192, 0,
                       224, 192,
                       128, 224, 192, 64, 96, 64, 192, 96, 64, 64, 224, 64, 192, 224, 64, 64, 96, 192, 192, 96, 192, 64,
                       224,
                       192, 192, 224, 192, 32, 32, 0, 160, 32, 0, 32, 160, 0, 160, 160, 0, 32, 32, 128, 160, 32, 128,
                       32, 160,
                       128, 160, 160, 128, 96, 32, 0, 224, 32, 0, 96, 160, 0, 224, 160, 0, 96, 32, 128, 224, 32, 128,
                       96, 160,
                       128, 224, 160, 128, 32, 96, 0, 160, 96, 0, 32, 224, 0, 160, 224, 0, 32, 96, 128, 160, 96, 128,
                       32, 224,
                       128, 160, 224, 128, 96, 96, 0, 224, 96, 0, 96, 224, 0, 224, 224, 0, 96, 96, 128, 224, 96, 128,
                       96, 224,
                       128, 224, 224, 128, 32, 32, 64, 160, 32, 64, 32, 160, 64, 160, 160, 64, 32, 32, 192, 160, 32,
                       192, 32,
                       160, 192, 160, 160, 192, 96, 32, 64, 224, 32, 64, 96, 160, 64, 224, 160, 64, 96, 32, 192, 224,
                       32, 192,
                       96, 160, 192, 224, 160, 192, 32, 96, 64, 160, 96, 64, 32, 224, 64, 160, 224, 64, 32, 96, 192,
                       160, 96,
                       192, 32, 224, 192, 160, 224, 192, 96, 96, 64, 224, 96, 64, 96, 224, 64, 224, 224, 64, 96, 96,
                       192, 224,
                       96, 192, 96, 224, 192, 0, 0, 0]

COCO_palette = [31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227,
                119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44,
                214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207,
                31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75,
                227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44,
                214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189,
                34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75,
                227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127,
                14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189,
                34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103,
                189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127,
                14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127
    , 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103,
                189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14,
                44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127,
                127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189,
                140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44,
                160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190,
                207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194,
                127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148,
                103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127,
                14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34,
                23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227,
                119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14, 44, 160, 44, 214, 39,
                40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127, 127, 188, 189, 34, 23, 190, 207, 31, 119,
                180, 255, 127, 14, 44, 160, 44, 214, 39, 40, 148, 103, 189, 140, 86, 75, 227, 119, 194, 127, 127,
                127, 188, 189, 34, 23, 190, 207, 31, 119, 180, 255, 127, 14]



# 给图像染色，mask类型为numpy
def colorize_mask(mask, palette):
    zero_pad = 256 * 3 - len(palette)
    for i in range(zero_pad):
        palette.append(0)
    new_mask = Image.fromarray(mask.astype(np.uint8)).convert('P')
    new_mask.putpalette(palette)
    return new_mask

# 根据RGB值将实例映射为一个整数ID
def re_id(matrix):
    # print(matrix)
    # return int(matrix)
    return matrix[0] * (256 * 256) + matrix[1] * 256 + matrix[2]


# 依据实例分割或者全景分割的标签得到细化后的伪标签
def get_fine_label(queue, queue_idx__img_paths):
    while True:
        idx, pseudo_label_path = queue_idx__img_paths.get()
        if idx is None or idx == '' or pseudo_label_path is None or \
                pseudo_label_path == '':
            break
        label_name = pseudo_label_path.split('/')[-1]
        # label_name = ''
        # for i in name.split('_'):
        #     if str(i) == 'gtFine':
        #         break
        #     label_name = label_name + str(i) + '_'
        # label_name = label_name + 'leftImg8bit.png'
        ins_label_path = os.path.join(ins_label_dir, label_name.replace('leftImg8bit', 'gtFine_panoptic'))
        save_path = os.path.join(save_dir, label_name.replace('leftImg8bit', 'gtFine_labelIds'))

        if os.path.exists(ins_label_path) == False:
            print(f'{ins_label_path}       不存在!!!!!')
            continue

        ins_dict.clear()
        ins_seg_match.clear()
        image = np.array(Image.open(ins_label_path))
        pseudo_label = np.array(Image.open(pseudo_label_path))
        print(f'正在处理伪标签:{pseudo_label_path}')
        copied_image = pseudo_label.copy()
        h, w = image.shape[0], image.shape[1]
        # print(f'{image.shape}   {pseudo_label.shape}')
        for i in range(h):
            for j in range(w):
                if re_id(image[i][j]) == 0:  # 背景区域不作处理
                    continue
                ID = re_id(image[i][j])  # 得到实例对应的唯一ID
                pse_label = pseudo_label[i][j]  # 得到该像素对应的伪标签
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
                # 对于cityscapes,0也应当被归为一种类别,并不能忽略他
                #if key2 != 0:
                if True:  # cityscapes 如此写

                    # 如果是高亮目标，扩大影响
                    if key2 in highlight_object:
                        tmp_dict[key2] = tmp_dict[key2] * beta
                    # 如果是弱化目标，削弱影响
                    if key2 in weaker_object:
                        tmp_dict[key2] = tmp_dict[key2] * gamma

                    if tmp_dict[key2] > max_num:
                        max_num = tmp_dict[key2]
                        max_key = key2
            if max_num == 0:  # or float(max_num) / float(count) < ALPHA:
                ins_seg_match[key1] = 0
            else:
                ins_seg_match[key1] = max_key

        # 遍历，生成细化后的伪标签
        for i in range(h):
            for j in range(w):
                ID = re_id(image[i][j])
                if ID == 0:
                    copied_image[i][j] = 0
                    continue
                copied_image[i][j] = ins_seg_match[ID]
        mask = colorize_mask(copied_image, CityScpates_palette)
        mask.save(save_path)


if __name__ == '__main__':
    src_path = pseudo_label_dir
    img_paths = [os.path.join(src_path, f) for f in os.listdir(src_path)]

    mp.set_start_method('spawn')

    queue_img = mp.Queue(64)
    queue_idx__img_path = mp.Queue(len(img_paths))
    [queue_idx__img_path.put(idx__img_path) for idx__img_path in enumerate(img_paths)]

    processes = list()
    for i in range(64):
        processes.append(mp.Process(target=get_fine_label, args=(queue_img, queue_idx__img_path)), )

    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    [process.join() for process in processes]

