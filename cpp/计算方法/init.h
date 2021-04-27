#include<iostream>

double*zeros1(int n){
    double*p;
    p=new double[n]();
    return p;
}

double*ones1(int n,double value=1.){
    double*p=zeros1(n);
    for(int i=0;i<n;i++){
        p[i]=value;
    }
    return p;
}

void MatShow(double*p,int n){
    std::cout<<std::endl;
    for(int i=0;i<n;i++){
        std::cout<<p[i]<<" "; 
    }
    std::cout<<std::endl;
}

double**zeros2(int m,int n){
    double**p;
    p=new double*[m];
    for(int j=0;j<m;j++){
        p[j]=new double[n]();
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

double**eye(int n){
    double**p=zeros2(n,n);
    for(int j=0;j<n;j++){
        p[j][j]=1.;
    }
    return p;
}

void MatShow(double**p,int m,int n){
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            if(i==0)std::cout<<std::endl;
            std::cout<<p[j][i]<<" ";
        }
    }
    std::cout<<std::endl;
}

double***zeros3(int l,int m,int n){
    double***p;
    p=new double**[l];
    for(int i=0;i<l;i++){
        p[i]=new double*[m];
        for(int j=0;j<m;j++){
            p[i][j]=new double[n]();
        }
    }
    return p;
}

double***ones3(int l,int m,int n,double value=1.){
    double***p=zeros3(l,m,n);
    for(int i=0;i<l;i++){
        for(int j=0;j<m;j++){
            for(int k=0;k<n;k++){
                p[i][j][k]=value;
            }
        }
    }
    return p;
}

class matrix{
    public:
        int m;
        int n;
        double**p;
        
        //构造函数
        matrix(int m=1,int n=1,double value=0.){
            this->p=ones2(m,n,value);
            this->m=m;
            this->n=n;
        }

        //析构函数
        ~matrix(){
            delete []p;
        };

        //矩阵显示
        void show(){
            MatShow(p,m,n);
        }

        //Transpose转置
        matrix Transpose(){
            matrix matT=matrix(this->n,this->m);
            for(int j=0;j<this->m;j++){
                for(int i=0;i<this->n;i++){
                    matT.p[i][j]=this->p[j][i];
                }
            }
            return matT;
        }
};