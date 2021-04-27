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
    return 0;
}