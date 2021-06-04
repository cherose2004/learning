function mat = Kpole( E , A , L )
%给出杆的局部坐标刚度矩阵
%   输入值：E弹性模量；A横截面积，L杆的长度
mat = [1 , 1 ; 1 , 1];
mat = mat.*E*A/L;
end

