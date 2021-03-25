#include<iostream>
#include<string>
using namespace std;
struct person{
    int height;
    int weight;
    string name;
    int age;
};
int main(){
    person bcy={
        183,
        80,
        "Bao Chenyu",
        21
    };
    cout<<"name:"<<bcy.name<<endl;
    cout<<"age:"<<bcy.age<<endl;
    cout<<"height:"<<bcy.height<<endl;
    cout<<"weight:"<<bcy.weight<<endl;
    return 0;
}
