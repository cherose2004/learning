public class MyComplex {
    double real;
    double imag;

    public MyComplex(double real , double imag){
        this.real = real;
        this.imag = imag;
    }
    public MyComplex plus(MyComplex x){
        MyComplex y = new MyComplex(this.real + x.real , this.imag + x.imag);
        return y;
    }
    public void Show(){
        System.out.print(real);
        System.out.print("+");
        System.out.print(imag);
        System.out.println("im");
    }
    public static void main(String[] args) throws Exception {
        System.out.println("Hello, World!");
        MyComplex a = new MyComplex(1. , 2.);
        MyComplex b = new MyComplex(3. , 4.);
        MyComplex c;
        c = a.plus(b);
        c.Show();
    }
}