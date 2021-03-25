#include<iostream>
const int N=10;
using namespace std;
int main(){
    int a[N]={0};
    a[1]=30;
    a[2]=27;
    for(int i=0;i<N;i++)cout<<a[i]<<endl;
    cout<<"Size of array is:"<<sizeof a<<endl;
    int n=(sizeof a)/(sizeof (int));
    cout<<"Number of elements is:"<<n<<endl;
    return 0;
}