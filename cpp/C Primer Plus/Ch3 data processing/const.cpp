#include<iostream>
const int m=1;
const int n=2;
using namespace std;
int main(){
    cout<<m<<endl;
    cout<<n<<endl;
    int a=1;
    const int b=a+1;
    cout<<b<<endl;
    a+=1;
    cout<<b<<endl;
    return 0;
}