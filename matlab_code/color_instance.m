% 导入数据
load data xfit yfit xdata_m ydata_m ydata_s xVdata yVdata xmodel ymodel ...
    ymodelL ymodelU c cint

% 读取图片  
img = imread('G:\DataSets/cityscapes/gtFine/train/dusseldorf/dusseldorf_000000_000019_gtFine_labelIds.png'); % 将'your_image.jpg'替换为你的图片文件名  
  
% 获取图片的大小  
[rows, cols, channels] = size(img);  
% 输出图片的大小  
fprintf('图片的大小是：%d x %d x %d\n', rows, cols, channels);  

save_image = zeros([size(img) ,3]);

color_count = 1;
% 创建一个空的 Map 对象  
myDict = containers.Map('KeyType', 'int32', 'ValueType', 'any');

% 输出所有像素的值  
for i = 1:rows  
    for j = 1:cols  
        
        if img(i,j) == 3
            continue
        end
      
        id = ID(img(i,j));
        exists = isKey(myDict, id);
       if exists == true
           value_ = myDict(id);
           save_image(i,j,1) = value_(1);
           save_image(i,j,2) = value_(2);
           save_image(i,j,3) = value_(3);
       else
           myDict(id) = ColorPM(color_count);
           value_ = myDict(id);
           color_count = color_count + 2;
           save_image(i,j,1) = value_(1);
           save_image(i,j,2) = value_(2);
           save_image(i,j,3) = value_(3);
       end
    end 
end

imshow(save_image);  

