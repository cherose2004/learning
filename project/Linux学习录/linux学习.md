# Linux学习

## 0.基础操作

- pwd：求出当前路径
- ls：a（显示隐藏文件）；l（列表展示）；*占位符；??占位符（像正则表达式）；[内]任意字符
- cd：进入目录，..返回上级目录，.当前目录；/目录;-返回上级目录
- tab：补全键
- touch：创建文件
- mkdir：创建文件夹（make directory）
- rm：移除文件，使用-d删除文件夹（或者-r）
- mv：移动：若——（也支持正则表达）

```bash
mv file path
```

- cp（copy）复制：也支持正则表达

```bash
cp file path
cp file path/new_file_name
```

- find：搜索

```bash
find path -name filename(精确搜索，或用正则表达式)
```

-i：忽略大小写
-name：通过名字搜索
-iname：忽略大小写的名字匹配搜索
-size：根据大小查找(+大于，-小于)
-user：所属人
-mmin：+-数字
-amin：上次文件被访问时间
-cmin：上次文件属性被修改时间
-type：文件类型，f文件d目录l链接文件
-a：同时满足
-o：或满足

- locate：定位文件
- cat/more：显示文件内容（-n显示行号）
- grep：抓取文本文件（-n行号，-v反向抓取，去除，如'#'注释行，-i忽略大小写）；^sth表示以此sth开头；sth$指以此为末尾的情形

```bash
grep sth filename
```

- echo：回响

```bash
echo sth > filename  #覆盖
echo sth >> filename  #追加
cmd >/>> filename  #将某个结果写入filename
```

- 管道：将命令输出作为某命令输入

```bash
grep file linux学习.md | more/cat #前输出作为后之输入
```

- ln：创建链接

```bash
ln sth link
```

## 1.权限

- r只读
- w编辑
- x可执行文件

chmod(change mod)改变mod

```bash
chmod [ugoal][+-=][rwx] filename
```