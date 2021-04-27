#include<iostream>

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
        ~matrix(){
            delete []p;
        };

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
            std::cout<<this->p[j][i]<<" ";
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
        std::cout<<"dimensions error when use '+' "<<std::endl;
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
        std::cout<<"dimensions error when use '+' "<<std::endl;
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
        std::cout<<"dimensions error when use '+' "<<std::endl;
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