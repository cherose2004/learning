#include<iostream>
#include<vector>
using namespace std;

template<class T>
class Table{
public:
    T a;
    T b;
    template<class T1>
    friend ostream& operator <<(ostream& o , const Table<T1>& t);
};
template<class T1>
ostream& operator <<(ostream& o , const Table<T1>& t){
    o << "长："<< t.a << "," << "宽：" << t.b << "\n";
    return o;
}

int main(){
    Table<int> t;
    t.a = 3;
    t.b = 4;
    cout<<t;
    return 0;
}