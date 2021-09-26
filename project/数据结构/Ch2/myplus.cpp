#include<iostream>
using namespace std;

void print(int* p , int k){
    std::cout<<"[ ";
    for(int i = 0 ; i < k ; i++){
        std::cout<<p[i]<<", ";
    }
    std::cout<<"\b\b ]\n";
}

int* myplus(int* a1 , int* a2 , int k1 , int k2){
    int k = k1>k2?k1:k2;
    int* p = new int[k+1];
    int* p1 = new int[k];
    int* p2 = new int[k];
    for(int i = 0 ; i < k ; i++){
        if(i < k1) p1[i] = a1[k1-1-i];
        if(i < k2) p2[i] = a2[k2-1-i];
    }
    int carry = 0;
    int s;
    for(int i = 0 ; i < k ; i++){
        s = carry + p1[i] + p2[i];
        p[k+1-1-i] = s%10;
        carry = s/10;
    }
    if(carry) p[0] = 1;
    return p;
}

int main(){
    int a1[] = {1,2,3,4,5,6,7};
    int a2[] = {1,2,1};
    int* p = myplus(a1 , a2 , 7 , 3);
    print(p , 8);
    return 0;
}