[toc]

# Vim学习笔记

![](https://img-blog.csdnimg.cn/20191219104939654.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3d3d19oZWxsb3dvcmxkX2NvbQ==,size_16,color_FFFFFF,t_70)

## 初步——三个模块

- ：q只读退出
- ：wq写入并退出
- ：v可视模式，V全行可视模式

## 进阶

### 1.基于单词的移动

preview current next

- b：至上一个单词开头
- w：至下一个单词开头
- ge：至上一个单词末尾
- e：至下一个单词末尾

### 2.查找字符

- f{char}：查找char变量
- F{char}：反向查找char变量
- t{char}：char前一个变量
- T{char}：反向查找char变量前一个字符
- ;：重复上一次查找
- ,：反方向上一次查找

she sells the seashells by the seashore;

### 3.文本对象

**重中之重**

- i：inside里面
- a：around环周

v+
- a)或ab：一对圆括号
- i)或ib：一对圆括号内

(just for test)

v+
- a}或aB：一对花括号
- i}或iB：一对花括号内

类似的还有：\>，'，"，`

t表示再html两个标签中\<\>something\<\>

v+
- iw：当前单词  word
- aw：当前单词以及空格
- iW：当前字符串  Words
- aW：当前字符串以及一个空格
- is：当前句子   sentence
- as：当前句子及一个空格
- ip：当前段落   paragraph
- ap：当前段落及一个空行

she sells the seashells by the seashore;

### 4.操作符待决模式

- d{motion}：删除（dd）删除一行
- c{motion}：修改（cc）修改一行
- y{motion}：复制（yy）复制一行
- v{motion}：可视模式

### 5.设置标记，快速回跳转

- m{mark}：设置标记
- `{mark}：跳转标记
- gg：返回开头

### 6.复制与粘贴

- y：复制
- p：粘贴

### 7.翻页设置

- ctl+u：上翻半页
- ctl+d：下翻半页

### 8.查找替换

- /{pattern}：查找，使用n跳转
- :%s/{pattern}/{string}/g：替换
