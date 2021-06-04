function K = getK( E , A , L , theta )
%直接给出某一角度下杆的刚度矩阵
%   依次输入：弹性模量E，截面积A，杆长L，角度theta
Kp = Kpole(E , A , L);
lambda = Direction(theta);
K = lambda.' * Kp * lambda;
end