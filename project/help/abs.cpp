#include<iostream>
using namespace std;

int FindWhereMax(int* p, int n){
    int pos = 0;
    for(int i = 1 ; i < n ; i++){
        if( p[pos] < p[i] ){
            pos = i;
        }
    }
    return pos;
}

int IsUnique(int* p, int n, int item){
    int num = 0;
    for(int i = 0 ; i < n ; i++){
        if( p[i] == item ){
            num += 1;
        }
    }
    if( num > 1 ) return 0;
    else return 1;
}

int ArrayAbs(int* p, int n){
    int* Item;
    int* CountItem;
    Item = new int[n];
    CountItem = new int[n];
    for(int i = 0 ; i < n ; i++){
        Item[i] = -1;
        CountItem[i] = 0;
    }

    for(int i = 0 ; i < n ; i++){
        for(int j = 0 ; j < n ; j++){
            if( p[i] == Item[j] ){
                CountItem[j] += 1;
                break;
            }
            else if( Item[j] == -1 ){
                Item[j] = p[i];
                CountItem[j] = 1;
                break;
            }
        }
    }

    int MaxID = FindWhereMax(CountItem, n);
    if( IsUnique(CountItem, n, CountItem[MaxID]) ){
        return Item[MaxID];
    }
    else{
        return -1;
    }
}

int main(){
    int set[17] = {1,2,4,2,3,3,3,3,3,3,4,4,4,4,5,4,4};
    cout<<ArrayAbs(set, 17)<<endl;
    return 0;
}