#include<iostream>
#include<iomanip>

class matrix{
    private:
        double**zeros2(int m,int n,double value=0.){
            double**p;
            p=new double*[m];
            for(int j=0;j<m;j++){
                p[j]=new double[n]();
            }
            for(int j=0;j<m;j++){
                for(int i=0;i<n;i++){
                    p[j][i]=value;
                }
            }
            return p;
            };
    public:
        int m;
        int n;
        double**p;

        //构造函数
        matrix(int m=1,int n=1,double value=0.){
            this->p=this->zeros2(m,n,value);
            this->m=m;
            this->n=n;
        }
        
        //拷贝构造函数
        matrix(const matrix &mat){
            this->m=mat.m;
            this->n=mat.n;
            this->p=zeros2(mat.m,mat.n);
            for(int j=0;j<this->m;j++){
                for(int i=0;i<this->n;i++){
                    this->p[j][i]=mat.p[j][i];
                }
            }
        }

        //析构函数
        ~matrix(){delete []p;};

        //算符重载
        matrix operator+(const matrix& mat2);
        matrix operator+(const double u);
        friend matrix operator+(const double u,matrix mat2);

        matrix operator-(const matrix& mat2);
        matrix operator-(const double u);
        friend matrix operator-(const double u,matrix mat2);

        matrix operator*(const matrix& mat2);
        matrix operator*(const double u);
        friend matrix operator*(const double u,matrix mat2);

        matrix operator/(const matrix& mat2);
        matrix operator/(const double u);
        friend matrix operator/(const double u,matrix mat2);

        bool operator==(const matrix &mat2);
        bool operator!=(const matrix &mat2){return !(*this==mat2);}

        //Transpose转置
        matrix Transpose();

        //矩阵显示
        void show();

        //点积
        matrix dot(matrix mat2);

        //判断是否为方阵
        bool isSquare(){if(m==n)return 1;else return 0;}

        //reshape重塑函数
       matrix reshape(int m1,int n1); 

       //add添加函数
       int add(double u,char layout);
       int add(matrix mat2,char layout);
};

//转置
matrix matrix::Transpose(){
    matrix matT=matrix(this->n,this->m);
    for(int j=0;j<this->m;j++){
        for(int i=0;i<this->n;i++){
            matT.p[i][j]=this->p[j][i];
        }
    }
    return matT;
}


//显示在控制台上
void matrix::show(){
    for(int j=0;j<this->m;j++){
        for(int i=0;i<this->n;i++){
            if(i==0)std::cout<<std::endl;
            std::cout<<std::setw(6)<<this->p[j][i]<<" ";
        }
    }
    std::cout<<std::endl;
}


//算符重载+
matrix matrix::operator+(const matrix& mat2){
    if(this->m==mat2.m&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<this->m;j++){
            for(int i=0;i<this->n;i++){
                Mat.p[j][i]=this->p[j][i]+mat2.p[j][i];
            }
        }
        return Mat;
    }
        else if(mat2.m==1&&this->n==mat2.n){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]+mat2.p[0][i];
            }
        }
        return Mat;
    }
    else if(this->m==mat2.m&&mat2.n==1){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]+mat2.p[j][0];
            }
        }
        return Mat;
    }
    else if(this->m==1&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=mat2.p[j][i]+this->p[0][i];
            }
        }
        return Mat;
    }
    else if(this->n==1&&this->m==mat2.m){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=mat2.p[j][i]+this->p[j][0];
            }
        }
        return Mat;
    }
    else{
        std::cout<<"dimensions error when use '+' "<<std::endl;
        matrix Mat=matrix(mat2.m,mat2.n);
        return Mat;
    }
}
//数加+
matrix matrix::operator+(const double u){
    matrix Mat=matrix(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            Mat.p[j][i]=p[j][i]+u;
        }
    }
    return Mat;
}
matrix operator+(const double u,matrix mat2){return mat2*u;}


//算符重载-
matrix matrix::operator-(const matrix& mat2){
    if(this->m==mat2.m&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<this->m;j++){
            for(int i=0;i<this->n;i++){
                Mat.p[j][i]=this->p[j][i]-mat2.p[j][i];
            }
        }
        return Mat;
    }
        else if(mat2.m==1&&this->n==mat2.n){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]-mat2.p[0][i];
            }
        }
        return Mat;
    }
    else if(this->m==mat2.m&&mat2.n==1){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]-mat2.p[j][0];
            }
        }
        return Mat;
    }
    else if(this->m==1&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=this->p[0][i]-mat2.p[j][i];
            }
        }
        return Mat;
    }
    else if(this->n==1&&this->m==mat2.m){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=this->p[j][0]-mat2.p[j][i];
            }
        }
        return Mat;
    }
    else{
        std::cout<<"dimensions error when use '-' "<<std::endl;
        matrix Mat=matrix(mat2.m,mat2.n);
        return Mat;
    }
}
//数减-
matrix matrix::operator-(const double u){
    matrix Mat=matrix(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            Mat.p[j][i]=p[j][i]-u;
        }
    }
    return Mat;
}
matrix operator-(const double u,matrix mat2){
    matrix Mat=matrix(mat2.m,mat2.n);
    for(int j=0;j<mat2.m;j++){
        for(int i=0;i<mat2.n;i++){
            Mat.p[j][i]=u-mat2.p[j][i];
        }
    }
    return Mat;
}


//算符重载*
matrix matrix::operator*(const matrix& mat2){
    if(this->m==mat2.m&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<this->m;j++){
            for(int i=0;i<this->n;i++){
                Mat.p[j][i]=this->p[j][i]*mat2.p[j][i];
            }
        }
        return Mat;
    }
        else if(mat2.m==1&&this->n==mat2.n){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]*mat2.p[0][i];
            }
        }
        return Mat;
    }
    else if(this->m==mat2.m&&mat2.n==1){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]*mat2.p[j][0];
            }
        }
        return Mat;
    }
    else if(this->m==1&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=this->p[0][i]*mat2.p[j][i];
            }
        }
        return Mat;
    }
    else if(this->n==1&&this->m==mat2.m){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=this->p[j][0]*mat2.p[j][i];
            }
        }
        return Mat;
    }
    else{
        std::cout<<"dimensions error when use '*' "<<std::endl;
        matrix Mat=matrix(mat2.m,mat2.n);
        return Mat;
    }
}
//数乘*
matrix matrix::operator*(const double u){
    matrix Mat=matrix(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            Mat.p[j][i]=p[j][i]*u;
        }
    }
    return Mat;
}
matrix operator*(const double u,matrix mat2){return mat2*u;}


//算符重载/
matrix matrix::operator/(const matrix& mat2){
    if(this->m==mat2.m&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<this->m;j++){
            for(int i=0;i<this->n;i++){
                Mat.p[j][i]=this->p[j][i]/mat2.p[j][i];
            }
        }
        return Mat;
    }
        else if(mat2.m==1&&this->n==mat2.n){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]/mat2.p[0][i];
            }
        }
        return Mat;
    }
    else if(this->m==mat2.m&&mat2.n==1){
        matrix Mat=matrix(m,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=this->p[j][i]/mat2.p[j][0];
            }
        }
        return Mat;
    }
    else if(this->m==1&&this->n==mat2.n){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=this->p[0][i]/mat2.p[j][i];
            }
        }
        return Mat;
    }
    else if(this->n==1&&this->m==mat2.m){
        matrix Mat=matrix(mat2.m,mat2.n);
        for(int j=0;j<mat2.m;j++){
            for(int i=0;i<mat2.n;i++){
                Mat.p[j][i]=this->p[j][0]/mat2.p[j][i];
            }
        }
        return Mat;
    }
    else{
        std::cout<<"dimensions error when use '/' "<<std::endl;
        matrix Mat=matrix(mat2.m,mat2.n);
        return Mat;
    }
}
//数除/
matrix matrix::operator/(const double u){
    matrix Mat=matrix(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            Mat.p[j][i]=p[j][i]/u;
        }
    }
    return Mat;
}
matrix operator/(const double u,matrix mat2){
    matrix Mat=matrix(mat2.m,mat2.n);
    for(int j=0;j<mat2.m;j++){
        for(int i=0;i<mat2.n;i++){
            Mat.p[j][i]=u/mat2.p[j][i];
        }
    }
    return Mat;
}

//算符重载==
bool matrix::operator==(const matrix &mat2){
    if(m==mat2.m&&n==mat2.n){
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                if(p[j][i]!=mat2.p[j][i])return 0;
            }
        }
        return 1;
    }
    else return 0;
}


//点积
matrix matrix::dot(matrix mat2){
    if(this->n==mat2.m){
        matrix Mat(this->m,mat2.n);
        double sum;
        for(int j=0;j<this->m;j++){
            for(int i=0;i<mat2.n;i++){
                sum=0;
                for(int k=0;k<this->n;k++){
                    sum+=this->p[j][k]*mat2.p[k][i];
                }
                Mat.p[j][i]=sum;
            }
        }
        return Mat;
    }
    else{
        matrix Mat;
        std::cout<<"dimensions error when use dot!"<<std::endl;
        return Mat;
    }
}


//reshape重塑函数
matrix matrix::reshape(int m1,int n1){
    if(m1*n1!=this->m*this->n){
        std::cout<<"dimensions error when reshape!"<<std::endl;
        matrix Mat;
        return Mat;
    }
    else{
        matrix Mat(m1,n1);
        int cur;
        int jj;
        int ii;
        for(int j=0;j<m1;j++){
            for(int i=0;i<n1;i++){
                cur=j*n1+i;
                jj=int(cur/n);
                ii=cur-jj*n;
                Mat.p[j][i]=this->p[jj][ii];
            }
        }
        return Mat;
    }
}

//add添加函数
int matrix::add(double u,char layout='c'){
    if(layout=='c'){
        matrix Mat=*this;
        this->p=this->zeros2(m+1,n);
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                this->p[j][i]=Mat.p[j][i];
            }
        }
        for(int i=0;i<n;i++){
            this->p[m][i]=u;
        }
        this->m+=1;
    }
    else{
        matrix Mat=*this;
        this->p=this->zeros2(m,n+1); 
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                this->p[j][i]=Mat.p[j][i];
            }
        }
        for(int j=0;j<m;j++){
            this->p[j][n]=u;
        }
        this->n+=1;
    }
    return 0;
}

int matrix::add(matrix mat2,char layout='c'){
    if(layout=='c'){
        if(this->n==mat2.n){
            matrix mat1=*this;
            this->m=mat1.m+mat2.m;
            this->p=zeros2(this->m,this->n);
            for(int j=0;j<this->m;j++){
                for(int i=0;i<this->n;i++){
                    if(j<mat1.m)this->p[j][i]=mat1.p[j][i];
                    else this->p[j][i]=mat2.p[j-mat1.m][i];
                }
            }
        }
        else std::cout<<"dimensons error when use add!"<<std::endl;
    }
    else{
        if(this->m==mat2.m){
            matrix mat1=*this;
            this->n=mat1.n+mat2.n;
            this->p=zeros2(this->m,this->n);
            for(int j=0;j<this->m;j++){
                for(int i=0;i<this->n;i++){
                    if(i<mat1.n)this->p[j][i]=mat1.p[j][i];
                    else this->p[j][i]=mat2.p[j][i-mat1.n];
                }
            }
        }
        else std::cout<<"dimensons error when use add!"<<std::endl;
    }
    return 0;
}


//单位矩阵
matrix eye(int n){
    matrix Mat(n,n);
    for(int j=0;j<n;j++){
        Mat.p[j][j]=1.;
    }
    return Mat;
}

//方阵
matrix square(int n,double value=0.){
    matrix Mat(n,n,value);
    return Mat;
}

//一维向量
matrix linspace(double beg,double en,double d,char layout='c'){
    int n=int((en-beg)/d);
    if(layout=='c'){
        matrix Mat(n,1);
        for(int j=0;j<n;j++){
            Mat.p[j][0]=beg+j*d;
        }
        return Mat;
    }
    else{
        matrix Mat(1,n);
        for(int i=0;i<n;i++){
            Mat.p[0][i]=beg+i*d;
        }
        return Mat;
    }
}

//一维向量另一种定义方式
matrix arange(double beg,double en,int n,char layout='c'){
    double d=(en-beg)/double(n);
    return linspace(beg,en,d,layout);
}
