function dire = Direction( theta )
%获得方向矩阵，2*4
%   输入值为theta角度
lam1 = cos(theta);
lam2 = sin(theta);
dire = [lam1 , lam2 , 0 , 0 ;
        0 , 0 , lam1 , lam2];
end