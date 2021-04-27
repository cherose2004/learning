#include<iostream>
#include"init.h"
using namespace std;

int main(){
    double*array;
    array=ones1(4,2.);
    cout<<array[3]<<endl;
    double**arr;
    arr=ones2(5,4,7);
    cout<<arr[1][2]<<endl;
    double***a;
    a=ones3(3,3,3,9);
    cout<<a[1][1][1]<<endl;
    double**eye3=eye(3);
    cout<<eye3[1][1]<<endl;
    MatShow(array,4);
    MatShow(eye3,3,3);
    return 0;
}