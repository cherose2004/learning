#include<iostream>
#include<regex>
using namespace std;
int main(){
    string str = "abc123@abc123.xyz123";
    regex r("[a-z0-9]+@[a-z0-9]+\\.[a-z0-9]+");
    cout<<regex_match(str , r)<<endl;
    return 0;
}