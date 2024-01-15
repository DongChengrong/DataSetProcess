import os
import shutil

IN_PATH = r'G:\DataSets\cityscapes\gtFine'
OUT_PATH = r'G:\DataSets\cityscapes\cityscapes_instance'

def samples_select(IN_PATH, OUT_PATH):
    # 将一个目录下的所有文件全部复制到指定文件夹
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    for item in os.listdir(IN_PATH):
        src_item = os.path.join(IN_PATH, item)

        if os.path.isdir(src_item):
            samples_select(src_item, OUT_PATH)
        else:
            dst_item = os.path.join(OUT_PATH, item)
            print(dst_item)
            shutil.copy(src_item, dst_item)

def select_instance_labels(IN_PATH, OUT_PATH):
    # 如果目标文件夹不存在，创建它
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    # 遍历所有的文件夹
    for file in os.listdir(IN_PATH):
        src_item = os.path.join(IN_PATH, file)

        if os.path.isdir(src_item):
            select_instance_labels(src_item, OUT_PATH)
        else:
            # 检查文件结尾是否是instance
            if file.endswith("instanceIds.png"):
                dst_item = os.path.join(OUT_PATH, file)
                print(dst_item)
                shutil.copy(src_item, dst_item)



if __name__ == '__main__':
    select_instance_labels(IN_PATH, OUT_PATH)