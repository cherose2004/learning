#include<vector>
using namespace std;
vector<double> RK4_iter(double xi,double yi,double(*f)(double x,double y),double h=0.01){
    double k1=f(xi,yi);
    double k2=f(xi+h/2,yi+k1*h/2);
    double k3=f(xi+h/2,yi+k2*h/2);
    double k4=f(xi+h,yi+k3*h);
    double xi_next=xi+h;
    double yi_next=yi+(k1+2*k2+2*k3+k4)*h/2;
    vector<double> next={xi_next,yi_next};
    return next;
}

int RK4(double x0,double y0,double(*f)(double x,double y),vector<double>&x,vector<double>&y,float final=5,double h=0.01){
    int N=int(final/h);
    x.push_back(x0);
    y.push_back(y0);
    for(int i=0;i<N-1;i++){
        vector<double> next=RK4_iter(x[i],y[i],f,h);
        x.push_back(next[0]);
        y.push_back(next[1]);
    }
    return 0;
}