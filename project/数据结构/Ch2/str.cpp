#include<iostream>
#include<string>
using namespace std;
int main(){
    string name;
    name = "hello world";
    cout<<name<<endl;
    cout<<*(name.end()-1)<<endl;
    return 0;
}