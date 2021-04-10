# 使用gnuplot绘制命令

先在cpp内把绘制的数据cout出来，大概如下：
```C++
for(int i=0;i<x.size;i++){
    cout<<x[i]<<' '<<y[i]<<endl;
}
```

然后命令行编译,输入到data.dat文件内,调用gnuplot

```bash
g++ -o data 文件名.cpp
./data>"data.dat"
gnuplot
```

在gnuplot里面进行绘制，可以直接include "脚本名"，或者命令如下：
```gnuplot
plot "data.dat" w l
set xlabel("x")
set ylabel("y")
set grid
replot
```