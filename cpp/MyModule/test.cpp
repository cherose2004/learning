#include<iostream>
#include"List.h"
using namespace std;
int main(){
    List<double> a;
    a.append(5.6);
    cout<<a[0]<<endl;
    a.append(4.4);
    cout<<a[1]<<endl;
    cout<<a.len()<<endl;
    a[0] += 1;
    cout<<a[0]<<endl;
    List<double> b(10);
    b[1] = 2.1;
    cout<<b[1]<<endl;
    cout<<a;
    double p[6] = {1.1,2.2,3.3,4.4,5.5,6.6};
    List<double> c(p , 6);
    cout<<c<<endl;
    cout<<c.connect(a.connect(c))<<endl;
    c.insert(5,3.3);
    c.del(3);
    cout<<c;
    cout<<c.where(3.3)<<endl;
}