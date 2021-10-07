#include<iostream>
#include<iomanip>
#include<cmath>


class Array;
class Matrix;

template<class T>
class List{

    protected:
        int length;
        T*p;
      
        //空列表构造函数，传入参数n
        void InitList(int n){
            p = new T[n];
        };

    public:
      
        //构造函数1
        List(int length = 0){
            this->length = length;
            if(length > 0) InitList(length);
        }
        //构造函数2
        List(T*point , int n){
            this->length = n;
            this->InitList(n);
            for(int i = 0 ; i < n ; i++)this->p[i] = point[i];
        }
        //构造函数3
        List(int length , T object){
            this->length = length;
            InitList(length);
            for(int i = 0 ; i < length ; i++)this->p[i] = object;
        }
        //拷贝构造函数
        List(const List<T> &ls){
            int n = ls.len();
            this->length = n;
            this->InitList(n);
            for(int i = 0 ; i < n ; i++){
                this->p[i] = ls[i];
            }
        };
        //析构函数
        ~List(){delete []p;};

        //获取列表长度
        int len()const{return this->length;};

        //重载算符[]
        T &operator[](const int k)const{
            if(k < -this->length || k > this->length-1)std::cout<<"error:bounds error of List"<<std::endl;
            int j = k % this->length;
            if(j > 0 || j == 0) return this->p[j];
            else return this->p[j + length];
        };
        //重载算符 =
        void operator=(const List<T> &ls){
            this->length = ls.len();
            this->p = new T[length];
            for(int i = 0 ; i < this->length ; i++){
                this->p[i] = ls[i];
            }
        };
        //算符重载==
        bool operator==(const List<T> &ls){
            if(this->length != ls.len())return 0;
            else{
                for(int i = 0 ; i < ls.len() ; i++){
                    if(this->p[i] != ls[i])return 0;
                }
                return 1;
            }
        }
        //算符重载!=
        bool operator!=(const List<T> &ls){
            if(this->length != ls.len())return 1;
            else{
                for(int i = 0 ; i < ls.len() ; i++){
                    if(this->p[i] != ls[i])return 1;
                }
                return 0;
            }
        }
        //重载算符<<
        template<class T1>
        friend std::ostream &operator<<(std::ostream &os , const List<T1> &ls); 

        //添加函数，在末尾添加
        void append(T object){
            if(this->length == 0){
                this->length = 1;
                this->p = new T[1];
                this->p[0] = object;
            }
            else{
                List<T> ls = *this;
                this->length++;
                this->p = new T[this->length];
                for(int i = 0 ; i < length-1 ; i++){this->p[i] = ls[i];};
                this->p[this->length - 1] = object;
            }
        };
        //删除函数，在末尾删除
        void pop(){
            List<T> ls = *this;
            this->length--;
            this->p = new T[this->length];
            for(int i = 0 ; i < length ; i++){this->p[i] = ls[i];};
        }
        //列表切片
        List<T> cut(int first , int last){
            List<T> ls(last - first);
            for(int i = 0 ; i < ls.len() ; i++)ls[i] = this->p[first + i];
            return ls;
        }
        //列表拼接
        List<T> connect(const List<T> &ls){
            List<T> LS(this->length + ls.len());
            for(int i = 0 ; i < LS.len() ; i++){
                if(i < this->length)LS[i] = this->p[i];
                else LS[i] = ls[i - this->length];
            };
            return LS;
        }
        //列表插入
        void insert(int pos , T object){
            List<T> ls1(this->cut(0 , pos));
            List<T> ls2(this->cut(pos , this->length));
            List<T> ls;
            ls.append(object);
            *this = ls1.connect(ls.connect(ls2));
        }
        //列表删除
        void del(int pos){
            List<T> ls1(this->cut(0 , pos));
            List<T> ls2(this->cut(pos+1 , this->length));
            *this = ls1.connect(ls2);
        }
        //列表查询是否拥有某元素
        bool have(T object){
            for(int i = 0 ; i < this->length ; i++){
                if(this->p[i] == object)return 1;
            }
            return 0;
        }
        //列表索引某元素的位置
        int where(T object){
            for(int i = 0 ; i < this->length ; i++){
                if(this->p[i] == object)return i;
            }
            return -1;
        }
        //反转函数
        List<T> inverse(){
            List<T> ls(this->length);
            for(int i = 0 ; i < ls.len() ; i++){
                ls[i] = this->p[ls.len() - 1 - i];
            }
            return ls;
        }
};

//算符重载<<
template<class T1>
std::ostream &operator<<(std::ostream &os , const List<T1> &ls){
    int n = ls.len();
    os<<"\n";
    for(int i = 0 ; i < n ; i++) os<<ls[i]<<" ";
    os<<"\n";
    return os;
}


/*
Array数组类型定义****************************************************************************************************
*/

class Array : public List<double>{
    public:
        
        //构造函数1
        Array(int length = 0){
            this->length = length;
            this->InitList(length);
        }
        //构造函数2
        Array(double*point , int length){
            this->length = length;
            this->InitList(length);
            for(int i = 0 ; i < length ; i++)this->p[i] = point[i];
        }
        //构造函数3
        Array(int length , double num){
            this->length = length;
            this->InitList(length);
            for(int i = 0 ; i < length ; i++)this->p[i] = num;
        }
        //析构函数
        ~Array(){};

        //点积dot
        double dot(Array a){
            if(this->length != a.len()){
                std::cout<<"dimensions error when use dot"<<std::endl;
                return 0.;
            }
            else{
                double sum = 0.;
                for(int i = 0 ; i < this->length ; i++){
                    sum += this->p[i] * a[i];
                }
                return sum;
            }
        }


/*
***************************************************************************************************************
算符重载
*/
        //算符重载+ a1+a2
        Array operator+(const Array &a){
            if(this->length != a.len()){
                std::cout<<"dimensions error when use +"<<std::endl;
                return *this;
            }
            else{
                Array arr(this->length);
                for(int i = 0 ; i < arr.len() ; i++) arr[i] = this->p[i] + a[i];
                return arr;
            }
        }
        template<class T1>
        //算符重载+ a1+num
        Array operator+(const T1 &num){
            Array arr(this->length);
            for(int i = 0 ; i < arr.len() ; i++) arr[i] = this->p[i] + double(num);
            return arr;
        }
        //算符重载+ +a
        Array operator+(){return *this;};
        template<class T1>
        //算符重载+ num+a
        friend Array operator+(const T1 &num , Array arr);
        template<class T1>
        //算符重载+= num 
        void operator+=(const T1 num){*this = *this + num;};
        //算符重载+= arr
        void operator+=(const Array arr){*this = *this + arr;};

        //算符重载- a1-a2
        Array operator-(const Array &a){
            if(this->length != a.len()){
                std::cout<<"dimensions error when use -"<<std::endl;
                return *this;
            }
            else{
                Array arr(this->length);
                for(int i = 0 ; i < this->length ; i++) arr[i] = this->p[i] - a[i];
                return arr;
            }
        }
        template<class T1>
        //算符重载- a-num
        Array operator-(const T1 num){
            Array arr(this->length);
            for(int i = 0 ; i < this->length ; i++) arr[i] = this->p[i] - num;
            return arr;
        }
        //算符重载- -a
        Array operator-(){
            Array arr(this->length);
            for(int i = 0 ; i < this-> length ; i++) arr[i] = - this->p[i];
            return arr;
        };
        template<class T1>
        //算符重载- num-a
        friend Array operator-(const T1 &num , Array arr);
        //算符重载-= a1 -= a2
        void operator-=(const Array &a){*this = *this - a;};
        template<class T1>
        //算符重载-= a1 -= num
        void operator-=(const T1 &num){*this = *this - num;};

        //算符重载* a1*a2
        Array operator*(const Array &a){
            if(this->length != a.len()){
                std::cout<<"dimensions error when use *"<<std::endl;
                return *this;
            }
            else{
                Array arr(this->length);
                for(int i = 0 ; i < this->length ; i++) arr[i] = this->p[i] + a[i];
                return arr;
            }
        }
        template<class T1>
        //算符重载* a1*num
        Array operator*(const T1 &num){
            Array arr(this->length);
            for(int i = 0 ; i < this->length ; i++) arr[i] = this->p[i] * num;
            return arr;
        }
        template<class T1>
        //算符重载* num*a1
        friend Array operator*(const T1 &num , Array arr);
        //算符重载 a1 *= a2
        void operator*=(const Array arr){*this = *this * arr;};
        template<class T1>
        void operator*=(const T1 num){*this = *this * num;};

        //算符重载 a1/a2
        Array operator/(const Array &a2){
            if(this->length != a2.len()){
                std::cout<<"dimensions error when use /"<<std::endl;
                return *this;
            }
            else{
                Array arr(this->length);
                for(int i = 0 ; i < this->length ; i++) arr[i] = this->p[i] / a2[i];
                return arr;
            }
        }
        //算符重载 a1/num
        template<class T1>
        Array operator/(const T1 &num){
            Array arr(this->length);
            for(int i = 0 ; i < this->length ; i++) arr[i] = this->p[i] / num;
            return arr;
        }
        //算符重载 num/a1
        template<class T1>
        friend Array operator/(const T1 &num , Array a);
        //算符重载 a1/=a2
        void operator/=(const Array &a2){*this = *this/a2;};
        template<class T1>
        void operator/=(const T1 &num){*this = *this / num;};

        //算符重载 a1^a2
        Array operator^(const Array &a){
            if(this->length != a.len()){
                std::cout<<"dimensions error when use ^"<<std::endl;
                return *this;
            }
            else{
                Array arr(this->length);
                for(int i = 0 ; i < this->length ; i++) arr[i] = pow(this->p[i] , a[i]);
                return arr;
            }
        }
        template<class T1>
        //算符重载 a^num
        Array operator^(const T1 &num){
            Array arr(this->length);
            for(int i = 0 ; i < this->length ; i++) arr[i] = pow(this->p[i] , num);
            return arr;
        }
        template<class T1>
        //算符重载 num^a
        friend Array operator^(const T1 &num , Array a);
        //算符重载 num^=a
        void operator^=(const Array a){*this = *this^a;};
        template<class T1>
        //算符重载 a^=num
        void operator^=(const T1 &num){*this = *this^num;};
/*
***********************************************************************************************************************************
算符重载
*/
        //取最大max
        double max(){
            double tmp = this->p[0];
            for(int i = 1 ; i < this->length ; i++){
                if(tmp > this->p[i]);
                else tmp = this->p[i];
            }
            return tmp;
        }
        //取最小min
        double min(){
            double tmp = this->p[0];
            for(int i = 1 ; i < this->length ; i++){
                if(tmp < this->p[i]);
                else tmp = this->p[i];
            }
            return tmp;
        }
        //取和sum
        double sum(){
            double sum = 0;
            for(int i = 0 ; i < this->length ; i++) sum += this->p[i];
            return sum;
        }
        //取均值mean
        double mean(){
            return this->sum() / this->length;
        }
        //方差var
        double var(){
            double aver = this->mean();
            double sum = 0;
            double tmp;
            for(int i = 0 ; i < this->length ; i++){
                tmp = this->p[i] - aver;
                sum += tmp*tmp;
            }
            return sum / (this->length - 1);
        }
};

template<class T1>
Array operator+(const T1 &num , Array arr){return arr + num;}

template<class T1>
Array operator-(const T1 &num , Array arr){return - (arr - num);};

template<class T1>
Array operator*(const T1 &num , Array arr){return arr * num;};

template<class T1>
Array operator/(const T1 &num , Array a){
    Array arr(a.len());
    for(int i = 0 ; i < a.len() ; i++){
        arr[i] = num / a[i];
    }
    return arr;
}

template<class T1>
Array operator^(const T1 &num , Array a){
    Array arr(a.len());
    for(int i = 0 ; i < a.len() ; i++) arr[i] = pow(num , a[i]);
    return arr;
}

/*
开始矩阵类型的定义******************************************************************************************************
*/

class Matrix : public List<Array>{
    public:

        //初始化函数1
        Matrix(int m , int n){
            this->length = m;
            this->InitList(m);
            for(int i  = 0 ; i < m ; i++){
                Array arr(n);
                this->p[i] = arr;
            }
        }
        
        //初始化函数2
        Matrix(int m , int n , double num){
            this->length = m;
            this->InitList(m);
            for(int i  = 0 ; i < m ; i++){
                Array arr(n , num);
                this->p[i] = arr;
            }
        }

        //初始化函数3,对于传统的参数需要指定(T*)arr
        template<class T>
        Matrix(T* a , int m , int n){
            this->length = m;
            this->InitList(m);
            for(int i = 0 ; i < m ; i++){
                Array arr(n);
                this->p[i] = arr;
            }
            for(int j = 0 ; j < m ; j++){
                for(int i = 0 ; i < n ; i++){
                    this->p[j][i] = *(a+j*n+i);
                }
            }
        }

        //初始化函数4，需要(*array)[N]这样给定
        template<class T>
        Matrix(T** a , int m , int n){
            this->length = m;
            this->InitList(m);
            for(int i = 0 ; i < m ; i++){
                Array arr(n);
                this->p[i] = arr;
            }
            for(int j = 0 ; j < m ; j++){
                for(int i = 0 ; i < n ; i++){
                    this->p[j][i] = *((a+i)+j*n);
                }
            }
        }

        //~析构函数
        ~Matrix(){};
};