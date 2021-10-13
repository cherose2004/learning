import java.util.ArrayList;
public class Hailstone {
    public static boolean IsOdd(int x) {
        if( x%2 == 1 ) return false;
        else return true;
    }
    public static int Next(int x) {
        if( IsOdd(x) == true ) return x/2;
        else return 3*x+1;
    }
    public static void main(String[] args) {
        ArrayList<Integer> Sequence = new ArrayList<>();
        int init = 18;
        int iter = init;
        Sequence.add(init);
        while(iter != 1){
            iter = Next(iter);
            Sequence.add(iter);
        }
        System.out.println(Sequence);
    }
}