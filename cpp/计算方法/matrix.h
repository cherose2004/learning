#include<iostream>
#include<iomanip>
#include<cmath>

class matrix{
    private:
        double**zeros2(int m,int n,double value=0.){
            double**p;
            p=new double*[m];
            for(int j=0;j<m;j++){
                p[j]=new double[n]();
            }
            if(value==0.)return p;
            else{
                for(int j=0;j<m;j++){
                    for(int i=0;i<n;i++){
                        p[j][i]=value;
                    }
                }
                return p;
            }
        }

        double pn(int j,int i){
            if((j+i)%2==0)return 1;
            else return -1;
        }

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

        matrix operator^(const double u);
        friend matrix operator^(const double u,matrix mat2);

        void operator=(const matrix &mat2);

        double operator()(const int j,int i);
        double operator[](const int k);

        //Transpose转置
        matrix Transpose();

        //矩阵显示
        void show();

        //点积
        matrix dot(matrix mat2);
        //次方
        matrix power(int k);

        //判断是否为方阵
        bool isSquare(){if(m==n)return 1;else return 0;}

        //reshape重塑函数
       matrix reshape(int m1,int n1); 

       //add添加函数
       int add(double u,char layout);
       int add(matrix mat2,char layout);
       
       //cut得到一个子矩阵
       matrix cut(int j1,int j2,int i1,int i2);
       matrix row(int j){return this->cut(j,j,0,n-1);};
       matrix col(int i){return this->cut(0,m-1,i,i);};
       void set_row(int j,matrix mat2);
       void set_col(int i,matrix mat2);
       void set_part(int j0,int i0,matrix mat2);

       //除去j行i列后的矩阵del
       matrix del(int j1,int i1);

       //det行列式值
       double det();

       //A伴随矩阵
       matrix A();

       //inv逆矩阵
       matrix inv();

       //max(),取最大值
       matrix max(char layout);
       //min(),取最小值
       matrix min(char layout);

       //sum，求和函数
       matrix sum(char layout);
       //prod,求积函数
       matrix prod(char layout);
       //mean均值函数
       matrix mean(char layout);

       //apply(f)函数应用
       void apply(double(*f)(double x));
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

//算符重载^
matrix matrix::operator^(const double u){
    matrix Mat(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            Mat.p[j][i]=pow(p[j][i],u);
        }
    }
    return Mat;
}

matrix operator^(const double u,matrix mat2){
    matrix Mat(mat2.m,mat2.n);
    for(int j=0;j<mat2.m;j++){
        for(int i=0;i<mat2.n;i++){
            Mat.p[j][i]=pow(u,mat2.p[j][i]);
        }
    }
    return Mat;
}

//=
void matrix::operator=(const matrix &mat2){
    this->m=mat2.m;
    this->n=mat2.n;
    this->p=zeros2(this->m,this->n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            this->p[j][i]=mat2.p[j][i];
        }
    }
}


//()
double matrix::operator()(const int j,int i=0){
    int j1=j%m;
    int i1=i%n;
    if(j1<0)j1+=m;
    if(i1<0)i1+=n;
    return this->p[j1][i1];
}

//[]
double matrix::operator[](const int k){
    int k1;
    if(k<0){
        k1=k%(m*n);
        if(k1<0)k1+=m*n;
    }
    else k1=k%(m*n);
    int j=k1%m;
    int i=k1/m;
    return this->p[j][i];
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

matrix eye(int n);
//次方
matrix matrix::power(int k){
    if(!(this->isSquare())){
        std::cout<<"is not a square when use pow!"<<std::endl;
        return *this;
    }
    else{
        matrix Mat=eye(m);
        for(int i=0;i<k;i++){
            Mat=Mat.dot(*this);
        }
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


//cut得到子矩阵
matrix matrix::cut(int j1=0,int j2=0,int i1=0,int i2=0){
    matrix Mat(j2-j1+1,i2-i1+1);
    for(int j=0;j<Mat.m;j++){
        for(int i=0;i<Mat.n;i++){
            Mat.p[j][i]=this->p[j1+j][i1+i];
        }
    }
    return Mat;
}

//set_row行赋值
void matrix::set_row(int j,matrix mat2){
    if(mat2.m==1&&mat2.n==this->n){
        for(int i=0;i<this->n;i++){
            this->p[j][i]=mat2.p[0][i];
        }
    }
    else{
        std::cout<<"dimensions error when use set_row()"<<std::endl;
    }
}

//set_col列赋值
void matrix::set_col(int i,matrix mat2){
    if(mat2.n==1&&mat2.m==this->m){
        for(int j=0;j<m;j++){
            this->p[j][i]=mat2.p[j][0];
        }
    }
    else{
        std::cout<<"dimensions error when use set_col()"<<std::endl;
    }
}

//set_part()部分赋值
void matrix::set_part(int j0,int i0,matrix mat2){
    for(int j=0;j<mat2.m;j++){
        for(int i=0;i<mat2.n;i++){
            this->p[j+j0][i+i0]=mat2.p[j][i];
        }
    }
}


//del删去j行i列后的matrix
matrix matrix::del(int j1,int i1){
    if(j1==0&&i1==0)return this->cut(1,m-1,1,n-1);
    else if(j1==0&&i1==n-1)return this->cut(1,m-1,0,n-2);
    else if(j1==m-1&&i1==0)return this->cut(0,m-2,1,n-1);
    else if(j1==m-1&&i1==n-1)return this->cut(0,m-2,0,n-2);
    else if(j1==0&&i1!=0&&i1!=n-1){
        matrix mat1=this->cut(1,m-1,0,i1-1);
        matrix mat2=this->cut(1,m-1,i1+1,n-1);
        mat1.add(mat2,'r');
        return mat1;
    }
    else if(j1==m-1&&i1!=0&&i1!=n-1){
        matrix mat1=this->cut(0,m-2,0,i1-1);
        matrix mat2=this->cut(0,m-2,i1+1,n-1);
        mat1.add(mat2,'r');
        return mat1;
    }
    else if(i1==0&&j1!=0&&j1!=m-1){
        matrix mat1=this->cut(0,j1-1,1,n-1);
        matrix mat2=this->cut(j1+1,m-1,1,n-1);
        mat1.add(mat2);
        return mat1;
    }
    else if(i1==n-1&&j1!=0&&j1!=m-1){
        matrix mat1=this->cut(0,j1-1,0,n-2);
        matrix mat2=this->cut(j1+1,m-1,0,n-2);
        mat1.add(mat2);
        return mat1;
    }
    else{
        matrix mat1=this->cut(0,j1-1,0,i1-1);
        matrix mat2=this->cut(0,j1-1,i1+1,n-1);
        matrix mat3=this->cut(j1+1,m-1,0,i1-1);
        matrix mat4=this->cut(j1+1,m-1,i1+1,n-1);
        mat1.add(mat3);
        mat2.add(mat4);
        mat1.add(mat2,'r');
        return mat1;
    }
}


//det()行列式值
double matrix::det(){
    if(this->isSquare()==0){
        std::cout<<"is not a square when use det!"<<std::endl;
        return 0;
    }
    else{
        if(m==1){return this->p[0][0];}
        else if(m==2){
            double a=this->p[0][0];
            double b=this->p[0][1];
            double c=this->p[1][0];
            double d=this->p[1][1];
            return a*d-b*c;
        }
        else{
            double sum=0;
            for(int k=0;k<n;k++){
                sum+=pn(0,k)*(this->del(0,k)).det()*(this->p[0][k]);
            }
            return sum;
        }
    }
}


//A伴随矩阵
matrix matrix::A(){
    matrix Mat(m,n);
    if(!this->isSquare()){
        std::cout<<"is not a square when use A()"<<std::endl;
        return Mat;
    }
    else{
        matrix mat=this->Transpose();
        for(int j=0;j<m;j++){
            for(int i=0;i<n;i++){
                Mat.p[j][i]=pn(j,i)*(mat.del(j,i)).det();
            }
        }
        return Mat;
    }
}

//inv逆矩阵
matrix matrix::inv(){
    double u=this->det();
    matrix Mat=this->A();
    return Mat/u;
}



//max(),按列取最大值
matrix matrix::max(char layout='c'){
    if(layout=='c'){
        matrix Mat(1,n);
        double Max;
        for(int i=0;i<n;i++){
            Max=p[0][i];
            for(int j=1;j<m;j++){
                if(p[j][i]>Max)Max=p[j][i];
                else;
            }
            Mat.p[0][i]=Max;
        }
        return Mat;
    }
    else{
        matrix Mat(m,1);
        double Max;
        for(int j=0;j<m;j++){
            Max=p[j][0];
            for(int i=1;i<m;i++){
                if(p[j][i]>Max)Max=p[j][i];
                else;
            }
            Mat.p[j][0]=Max;
        }
        return Mat;
    }
}

//min(),取最小值
matrix matrix::min(char layout='c'){
    if(layout=='c'){
        matrix Mat(1,n);
        double Min;
        for(int i=0;i<n;i++){
            Min=p[0][i];
            for(int j=1;j<m;j++){
                if(p[j][i]<Min)Min=p[j][i];
                else;
            }
            Mat.p[0][i]=Min;
        }
        return Mat;
    }
    else{
        matrix Mat(m,1);
        double Min;
        for(int j=0;j<m;j++){
            Min=p[j][0];
            for(int i=1;i<m;i++){
                if(p[j][i]<Min)Min=p[j][i];
                else;
            }
            Mat.p[j][0]=Min;
        }
        return Mat;
    }
}



//sum,求和函数
matrix matrix::sum(char layout='c'){
    if(layout=='c'){
        matrix Mat(1,n);
        double s;
        for(int i=0;i<n;i++){
            s=0;
            for(int j=0;j<m;j++){
                s+=p[j][i];
            }
            Mat.p[0][i]=s;
        }
        return Mat;
    }
    else{
        matrix Mat(m,1);
        double s;
        for(int j=0;j<m;j++){
            s=0;
            for(int i=0;i<n;i++){
                s+=p[j][i];
            }
            Mat.p[j][0]=s;
        }
        return Mat;
    }
}

//prod求积函数
matrix matrix::prod(char layout='c'){
    if(layout=='c'){
        matrix Mat(1,n);
        double s;
        for(int i=0;i<n;i++){
            s=1;
            for(int j=0;j<m;j++){
                s*=p[j][i];
            }
            Mat.p[0][i]=s;
        }
        return Mat;
    }
    else{
        matrix Mat(m,1);
        double s;
        for(int j=0;j<m;j++){
            s=1;
            for(int i=0;i<n;i++){
                s*=p[j][i];
            }
            Mat.p[j][0]=s;
        }
        return Mat;
    }
}


//mean均值函数
matrix matrix::mean(char layout='c'){
    if(layout=='c'){
        matrix Mat=this->sum('c')/double(m);
        return Mat;
    }
    else{
        matrix Mat=this->sum('r')/double(n);
        return Mat;
    }
}


//apply(f)映射函数
void matrix::apply(double(*f)(double x)){
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            this->p[j][i]=f(this->p[j][i]);
        }
    }
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


//构造矩阵并返回
matrix make_mat(double *p,int m,int n){
    matrix Mat(m,n);
    for(int j=0;j<m;j++){
        for(int i=0;i<n;i++){
            Mat.p[j][i]=*(p+j*n+i);
        }
    }
    return Mat;
}


//取最大值
double max(matrix mat){
    matrix mat1=mat.max('r');
    matrix mat2=mat1.max('c');
    return mat2.p[0][0];
}

//取最小值
double min(matrix mat){
    matrix mat1=mat.min('r');
    matrix mat2=mat1.min('c');
    return mat2.p[0][0];
}


//求和
double sum(matrix mat){
    matrix mat1=mat.sum('r');
    matrix mat2=mat1.sum('c');
    return mat2.p[0][0];
}

//求积
double prod(matrix mat){
    matrix mat1=mat.prod('r');
    matrix mat2=mat1.prod('c');
    return mat2.p[0][0];
}


//求均值
double mean(matrix mat){
    return sum(mat)/double(mat.m*mat.n);
}


//作用函数
matrix apply(matrix mat,double(*f)(double x)){
    matrix Mat=mat;
    Mat.apply(f);
    return Mat;
}