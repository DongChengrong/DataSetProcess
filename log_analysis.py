import re

# 从文件中读取文本数据
with open(r'G:\实验数据\FedMTL实验数据\split5\log_fedavg.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    print(data)

# 使用正则表达式提取"EVAL"行中的"Mean IoU"
# pattern = r'EVAL \(\d+\) \|  PixelAcc: \d+\.\d+, Mean IoU: (\d+\.\d+) \|'
pattern = r"Mean IoU: (\d+\.\d+)"
mean_iou_matches = re.findall(pattern, data)

# 输出提取到的所有"EVAL"行的"Mean IoU"
index = 0
miou_list = [[],[],[],[],[],[],[],[],[], [],[]]
for mean_iou in mean_iou_matches:
    miou_list[index].append(round(float(mean_iou) *100, 1))
    index = index + 1
    if index == 6:
        index = 0

print(miou_list)
for item in miou_list:
    print(item)