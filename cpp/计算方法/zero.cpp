#include<iostream>

double*zeros1(int m){
    double*p;
    p=new double[m]();
    return p;
}

double**zeros2(int m,int n){
    double**p;
    p=new double*[m];
    for(int i=0;i<m;i++){
        p[i]=new double[n]();
    }
    return p;
}

double***zeros3(int m,int n,int l){
    double***p;
    p=new double**[m];
    for(int i=0;i<m;i++){
        p[i]=new double*[n];
        for(int j=0;j<n;j++){
            p[i][j]=new double[l]();
        }
    }
    return p;
}

int main(){
    double*array;
    array=zeros1(4);
    std::cout<<array[3]<<std::endl;
    double**arr;
    arr=zeros2(5,4);
    std::cout<<arr[1][2]<<std::endl;
    double***a;
    a=zeros3(3,3,3);
    std::cout<<a[1][1][1]<<std::endl;
    return 0;
}