#include<iostream>
#define pi 3.1415926 
#define g 9.8
using namespace std;
int main(){
    for(int i=0;i<10000;i++){
        float t=float(i)/10000;
        cout<<20*t<<' ';
        cout<<-g*t*t/2<<endl;
    }
    return 0;
}
