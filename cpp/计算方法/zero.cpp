#include<iostream>

double*zeros1(int m){
    double*p;
    p=new double[m]();
    return p;
}

double*ones1(int m,double value=1.){
    double*p=zeros1(m);
    for(int i=0;i<m;i++){
        p[i]=value;
    }
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

double**ones2(int m,int n,double value=1.){
    double**p=zeros2(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            p[j][i]=value;
        }
    }
    return p;
}

double**eye(int m){
    double**p=zeros2(m,m);
    for(int i=0;i<m;i++){
        for(int j=0;j<m;j++){
            if(i==j){
                p[i][j]=1.;
            }
        }
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

double***ones3(int m,int n,int l,double value=1.){
    double***p=zeros3(m,n,l);
    for(int i=0;i<m;i++){
        for(int j=0;j<n;j++){
            for(int k=0;k<l;k++){
                p[i][j][k]=value;
            }
        }
    }
    return p;
}

int main(){
    double*array;
    array=ones1(4,2.);
    std::cout<<array[3]<<std::endl;
    double**arr;
    arr=ones2(5,4,7);
    std::cout<<arr[1][2]<<std::endl;
    double***a;
    a=ones3(3,3,3,9);
    std::cout<<a[1][1][1]<<std::endl;
    double**eye3=eye(3);
    std::cout<<eye3[1][1]<<std::endl;
    return 0;
}