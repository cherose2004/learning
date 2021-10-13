import java.util.Scanner;
public class RightTriangle {
    public static int FindMax(int a, int b, int c) {
        if( (a > b || a == b) && (a > c || a == c) ) return a;
        if( b > c || b == c ) return b;
        return c;
    }
    public static int FindMin(int a, int b, int c) {
        if( (a < b || a == b) && (a < c || a == c) ) return a;
        if( b < c || b == c ) return b;
        return c;
    }
    public static int FindMid(int a, int b, int c) {
        int max = FindMax(a, b, c);
        int min = FindMin(a, b, c);
        if( max != a && min != a) return a;
        if( max != b && min != b) return b;
        return c;
    }
    public static int IsRightTriangle(int a, int b, int c) {
        int x = FindMax(a, b, c);
        int y = FindMin(a, b, c);
        int z = FindMid(a, b, c);
        if( x*x == (y*y + z*z) ) return 1;
        else return 0;
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        int c = sc.nextInt();
        if( IsRightTriangle(a, b, c) == 1 ) System.out.println("Yes");
        else System.out.println("No");
    }
}