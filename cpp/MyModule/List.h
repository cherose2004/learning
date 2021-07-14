#include<iostream>
#include<iomanip>

template<class T>
class List{
    private:
        int length;
        T*p;
      
        //空列表构造函数，传入参数n
        void InitList(int n){
            T*p = NULL;
            p = new T[n];
        };
    public:
      
        //构造函数
        List(int length = 0){
            this->length = length;
            if(length > 0) InitList(length);
        }
        //拷贝构造函数
        List(const List &ls){
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

        //算符重载[]
        T &operator[](const int k)const{
            int j = k % this->length;
            if(j > 0 || j == 0) return this->p[j];
            else return this->p[j + length];
        };
        //重载算符 =
        void operator=(const List &ls){
            this->length = ls.len();
            this->p = new T[length];
            for(int i = 0 ; i < this->length ; i++){
                this->p[i] = ls[i];
            }
        };

        //添加函数，在末尾添加
        void append(T object){
            if(this->length == 0){
                this->length = 1;
                this->p = new T[1];
                this->p[0] = object;
            }
            else{
                List<T> ls;
                ls = *this;
                this->length++;
                this->p = new T[this->length];
                for(int i = 0 ; i < length-1 ; i++){this->p[i] = ls[i];};
                this->p[this->length - 1] = object;
            }
        };
        //删除函数，在末尾删除
        void pop(){
            List<T> ls;
            ls = *this;
            this->length--;
            this->p = new T[this->length];
            for(int i = 0 ; i < length ; i++){this->p[i] = ls[i];};
        }
};