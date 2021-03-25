#include <iostream>
using namespace std;
union ccc{
    int a;
    double b;
    long long c;
};
int main(){
    ccc p;
    p.a=20;
    p.b=3;
    p.c=100000;
    cout<<p.a<<endl<<p.b<<endl<<p.c<<endl;
    return 0;
}