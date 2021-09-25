import java.util.ArrayList;

class Student{
    public String id;
    public String name;
    public String toString(){
        return ("\n("+id+","+name+")\n") ;
    };
}

class Table<T>{
    public T a;
    public T b;
}

public class tem{
    public static void main(String[] args){
        Table<Integer> t = new Table<>();
        t.a = 3;
        t.b = 4;
        Table<Double> t2 = new Table<>();
        t2.a = 3.5;
        t2.b = 4.0;

        ArrayList<Student> al = new ArrayList<>();
        Student zs = new Student();
        zs.id = "S001";
        zs.name = "张三";
        al.add(zs);
        System.out.println(al);
    }
}