function id = ID(matrix)

% 判断通道数量
if isinteger(matrix)  
    id = int32(matrix);
else   
    id = int32(matrix(1) * (256 * 256) + matrix(2) * 256 + matrix(3));
end