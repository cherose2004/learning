- short 16
- int 至少和short一样长
- long 32至少和int一样长,-32768~+32768
- long long 64至少和long一样长

一些东西如CHAR_BIT是内置了大小的，表示char的位数
类似的还有MAX，MIN分别表示某种数据类型的最大值和最小值
需要#include\<climits>语句

unsigned类型没有符号，因此范围为0-65535