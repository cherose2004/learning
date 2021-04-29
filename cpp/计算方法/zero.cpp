#include<iostream>
#include"matrix.h"
using namespace std;

int main(){
    double a[4][4]={
        {1,1,3,4},
        {7,1,1,3},
        {3,2,1,3},
        {1,1,7,8},
    };
    matrix mat=make_mat((double*)a,4,4);
    mat.show();
    mat.dot(mat).show();
    power(mat,2).show();
    return 0;
}