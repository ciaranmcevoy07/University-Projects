import java.util.*;

public class Main {
    public static void main(String[] args) {
        dados d = new dados();
        List<List<Integer>> pl = d.postinglists();
        HashMap<String, List<Integer>> dict = d.dicionario(pl);
        List<Integer> s = d.search(dict);
        List<Integer> s2 = d.search2(dict);
        System.out.println(s);
        System.out.println(s2);
    }
    
}
