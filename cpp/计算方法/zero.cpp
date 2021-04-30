#include<iostream>
#include"matrix.h"
using namespace std;

double f(double x){
    return x*x;
}

int main(){
    double a[4][4]={
        {1,1,3,4},
        {7,1,1,3},
        {3,2,1,3},
        {1,1,7,8},
    };
    matrix mat=make_mat((double*)a,4,4);
    mat.show();
    apply(mat,f).show();
    mat.apply(f);
    mat.show();
    return 0;
}