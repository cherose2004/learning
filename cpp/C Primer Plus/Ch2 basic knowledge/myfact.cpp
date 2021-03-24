#include <iostream>
using namespace std;
int my_fact(int n){
    if(n==0||n==1)return 1;
    else{
        return my_fact(n-1)*n;
    };
}
int main(void){
    cout<<"5!="<<my_fact(5)<<endl;
}