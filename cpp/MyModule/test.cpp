#include<iostream>
#include"List.h"
using namespace std;
int main(){
    List<double> a;
    a.append(5.6);
    cout<<a[0]<<endl;
}