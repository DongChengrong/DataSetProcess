import shutil
import os

LABEL_PATH = r'G:\DataSets\PascalVOC\VOCdevkit\VOC2011\ImageSets\Segmentation\val.txt'
IMAGE_PATH = r'G:\DataSets\dongchengrong_3b7c441\ADE20K_2021_17_01\images\ADE\training'
OUT_PATH = r'G:\DataSets\FedMSL\global_test\image'
src_folder = r'G:\DataSets\cityscapes\gtFine\val'
dst_folder = r'G:\DataSets\cityscapes\annotation\val'

# 按照标签将有标签数据从无标签数据中摘出来
def select_labeled_data():
    with open(LABEL_PATH, 'r') as f:
        line = f.readline().strip()
        while line:
            id = str(line) + '.jpg'
            image_path = os.path.join(IMAGE_PATH, id)
            print(image_path)
            shutil.copy(image_path, OUT_PATH)
            line = f.readline().strip()

def search(src_folder, dst_folder):
    # 遍历源文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(src_folder):
        # 遍历当前文件夹中的所有文件
        for file in files:
            # 如果当前项是一个文件并且它的扩展名是".jpg"，就将它复制到目标文件夹中
            if file.endswith('.png') and 'labelIds.png' in str(file).split('_'):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_folder, file)
                print(f'{src_file}     {dst_file}')
                shutil.copy2(src_file, dst_file)
        # 遍历当前文件夹中的所有子文件夹，并递归地调用搜索函数
        for dir in dirs:
            src_subfolder = os.path.join(root, dir)
            search(src_subfolder, dst_folder)

if __name__ == '__main__':
    search(src_folder, dst_folder)