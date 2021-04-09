#include<vector>
using namespace std;

template<typename T,typename T2>
vector<T> RK4_iter(T xi,T yi,T(*f)(T x,T y),T2 h=0.01){
    T k1=f(xi,yi);
    T k2=f(xi+h/2,yi+k1*h/2);
    T k3=f(xi+h/2,yi+k2*h/2);
    T k4=f(xi+h,yi+k3*h);
    T xi_next=xi+h;
    T yi_next=yi+(k1+2*k2+2*k3+k4)*h/6;
    vector<T> next={xi_next,yi_next};
    return next;
}

template<typename T,typename T2,typename T3>
int RK4(T x0,T y0,T(*f)(T x,T y),vector<T>&x,vector<T>&y,T3 final=5,T2 h=0.01){
    int N=int(final/h);
    x.push_back(x0);
    y.push_back(y0);
    for(int i=0;i<N-1;i++){
        vector<T> next=RK4_iter(x[i],y[i],f,h);
        x.push_back(next[0]);
        y.push_back(next[1]);
    }
    return 0;
}

template<typename T,typename T2>
vector<T> RK4_iter_2(T xi,T yi,T y1i,T(*f)(T x,T y,T y1),T2 h=0.01){
    T k1=f(xi,yi,y1i);
    T k2=f(xi+h/2,yi+y1i*h/2,y1i+k1*h/2);
    T k3=f(xi+h/2,yi+y1i*h/2+k1*h*h/4,y1i+k2*h/2);
    T k4=f(xi+h,yi+y1i*h/2+k2*h*h/2,y1i+k3*h);
    T xi_next;
    xi_next=xi+h;
    T yi_next;
    yi_next=yi+y1i*h+h*h/6*(k1+k2+k3);
    T y1i_next;
    y1i_next=y1i+h/6*(k1+2*k2+2*k3+k4);
    vector<T> next={xi_next,yi_next,y1i_next};
    return next;
}

template<typename T,typename T2,typename T3>
int RK4_2(T x0,T y0,T y10,T(*f)(T x,T y,T y1),vector<T>&x,vector<T>&y,vector<T>&y1,T3 final=5,T2 h=0.01){
    int N=int(final/h);
    x.push_back(x0);
    y.push_back(y0);
    y1.push_back(y10);
    for(int i=0;i<N-1;i++){
        vector<T> next=RK4_iter_2(x[i],y[i],y1[i],f,h);
        x.push_back(next[0]);
        y.push_back(next[1]);
        y1.push_back(next[2]);
    }
    return 0;   
}