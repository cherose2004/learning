#include<iostream>
#include"List.h"
using namespace std;
int main(){
    List<double> a;
    a.append(5.6);
    cout<<a[0]<<endl;
    a.append(4.4);
    cout<<a[1]<<endl;
    a.pop();
    cout<<a.len()<<endl;
    a[0] += 1;
    cout<<a[0]<<endl;
    List<double> b(2);
    b[0] = 1;
    b[1] = 2;
    cout<<b.len()<<endl;
}