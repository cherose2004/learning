#include <iostream>
#include <vector>
using namespace std;

template<class T>
ostream& operator << (ostream& o , const vector<T>& array){
    o<<"[";
    for(auto x : array){
        o<<x<<",";
    }
    o<<"]";
    return o;
}

void func(int (*) [5] , int);
void func(int (*p)[5] , int k){
    cout<<"hello world"<<endl;
}

int main(){
    vector<double> array{1,2,3,4,5,6,7};
    cout<<array<<endl;
    int a[3][5];
    int(*p)[5];  //*p是个指针，[5]表明其指向有五个元素的数组
    p = a;
    return 0;
}