#include<iostream>
#include"matrix.h"
using namespace std;

int main(){
    matrix mat(3,3,900);
    mat.show();
    matrix matT=mat.Transpose();
    matT.show();
    matrix mat2(3,1,200);
    (0-mat).show();
    cout<<(mat!=matT)<<endl;
    matrix eye3=eye(3);
    eye3.show();
    (3*(mat2.Transpose()).dot(mat2)).show();
    (arange(0,10,100,'r')).show();
    std::cout<<mat2.isSquare()<<std::endl;
    (mat.reshape(1,9)).show();
    mat.add(3.);
    mat.show();
    mat.add(1,'r');
    mat.show();
    mat.add(mat,'r');
    mat.show();
    return 0;
}