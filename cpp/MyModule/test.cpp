#include <iostream>
#include "MyModule.h"
using namespace std;
int main(){
    List<double> a;
    a.append(5.6);
    cout<<a[0]<<endl;
    a.append(4.4);
    cout<<a[1]<<endl;
    cout<<a.len()<<endl;
    a[0] += 1;
    cout<<a[0]<<endl;
    List<double> b(10);
    b[1] = 2.1;
    cout<<b[1]<<endl;
    cout<<a;
    double p[6] = {1.1,2.2,3.3,4.4,5.5,6.6};
    List<double> c(p , 6);
    cout<<c<<endl;
    cout<<c.connect(a.connect(c))<<endl;
    c.insert(5,3.3);
    c.del(3);
    cout<<c;
    cout<<c.where(3.3)<<endl;
    List<double> d(10 , 8.8);
    cout<<d;
    cout<<c.inverse();

    cout<<"bellow is the test for array******************************************************************"<<endl;

    Array e;
    e.append(1.);
    e.append(2.);
    cout<<e.dot(e)<<endl;
    Array f(10);
    cout<<(f+10);
    f += 10.;
    cout<<f<<endl;
    Array g = 3-f;
    cout<<g<<endl;
    Array h = g*g;
    cout<<g<<endl;
    cout<<((g+9)^2.5)<<endl;

    cout<<"below is the test for matrix*****************************************************************"<<endl;

    Matrix k(4,10,3);
    cout<<k<<endl;
    cout<<k[0][-1]<<endl;
    double L[2][4] = {
        {1,2,3,4},
        {5,3,6,7}
    };
    Matrix M((double*)L , 2 , 4);
    cout<<M<<endl;
    Matrix NN(M);
    cout<<NN<<endl;
    return 0;
}