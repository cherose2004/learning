#include<iostream>
#include<vector>
#include<fstream>
#include<cmath>
#include "RK4.h"
#define g 9.8
#define k 0.03
using namespace std;

double func(double x,double y,double y1){
    return -g-k*y1*abs(y1);
}

int main(){
    vector<double> t;
    vector<double> y;
    vector<double> vy;
    RK4_2(0.,1000.,0.,func,t,y,vy,10,0.01);
    for(auto i:t)cout<<i<<" ";
    cout<<endl;
    for(auto i:y)cout<<i<<" ";
    cout<<endl;
    for(auto i:vy)cout<<i<<" ";
    cout<<endl;
    return 0;
}