#include<iostream>
#include<vector>
#include<fstream>
#define g 9.8
#define t 10.0
#define dt 0.01
#define N 10000
#define vx0 500
#define y0 100
//定义宏
using namespace std;

//迭代函数，运用欧拉法
vector<float> iter_func(float x,float y,float vx,float vy){
    vector<float> tmp(4,0.0);
    x+=vx*dt;
    y+=vy*dt;
    vx=vx;
    vy+=-g*dt;
    tmp[0]=x;
    tmp[1]=y;
    tmp[2]=vx;
    tmp[3]=vy;
    return tmp;
}

//仿真开始，调用迭代函数，不断向四个向量中推入迭代值
//在y<0的时候结束
int simulation(vector<float> &x,vector<float> &y,vector<float> &vx,vector<float> &vy){
    for(int i=0;i<N;i++){
        vector<float> next(4,0.0);
        next=iter_func(x[i],y[i],vx[i],vy[i]);
        if(next[1]<0)return i;
        x.push_back(next[0]);
        y.push_back(next[1]);
        vx.push_back(next[2]);
        vy.push_back(next[3]);
    }
    return 0;
}

int main(){
    vector<float> x(1,0.0);
    vector<float> y(1,0.0);
    vector<float> vx(1,0.0);
    vector<float> vy(1,0.0);
    vector<float> time(1,0.0);
    vx[0]=vx0;
    y[0]=100;
    //上述步骤是初始化
    int stop=simulation(x,y,vx,vy);//仿真开始
    //获取时序t
    for(int i=0;i<stop;i++){
        time.push_back(i*dt);
    }
    //打开记事本，把数据写入文件OTM_cpp_data.txt
    ofstream data;
    data.open("OTM_cpp_data.txt");
    for(auto i:time)data<<i<<' ';
    data<<endl;
    for(auto i:x)data<<i<<' ';
    data<<endl;
    for(auto i:y)data<<i<<' ';
    data<<endl;
    for(auto i:vx)data<<i<<' ';
    data<<endl;
    for(auto i:vy)data<<i<<' ';
    data<<endl;
    data.close();
    cout<<"success"<<endl;//在控制台上显示运行成功
    return 0;
}