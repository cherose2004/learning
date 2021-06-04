function Kout = Addpole(K , Kij , i , j)
%在杆系的K矩阵中加入i,j号位置的kij刚度矩阵
Kout = K;
i = i - 1;
j = j - 1;
kii = Kij(1:2 , 1:2);
kjj = Kij(3:4 , 3:4);
kij = Kij(3:4 , 1:2);
kji = Kij(1:2 , 3:4);
Kout(2*i+1 : 2*i+2 , 2*i+1 : 2*i+2) = K(2*i+1 : 2*i+2 , 2*i+1 : 2*i+2) + kii;
Kout(2*j+1 : 2*j+2 , 2*j+1 : 2*j+2) = K(2*j+1 : 2*j+2 , 2*j+1 : 2*j+2) + kjj;
Kout(2*i+1 : 2*i+2 , 2*j+1 : 2*j+2) = K(2*i+1 : 2*i+2 , 2*j+1 : 2*j+2) + kij;
Kout(2*j+1 : 2*j+2 , 2*i+1 : 2*i+2) = K(2*j+1 : 2*j+2 , 2*i+1 : 2*i+2) + kji;
end