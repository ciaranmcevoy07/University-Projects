import java.util.*;

public class dados {
    public List<List<Integer>> postinglists(){
        List<Integer> p1 = new ArrayList<>();
        List<Integer> p2 = new ArrayList<>();
        List<Integer> p3 = new ArrayList<>();
        ArrayList<List<Integer>> tudo = new ArrayList<>();
        p1.add(1);
        p1.add(2);
        p1.add(4);
        p1.add(11);
        p1.add(31);
        p1.add(45);
        p1.add(173);
        p1.add(174);
        p2.add(1);
        p2.add(2);
        p2.add(4);
        p2.add(5);
        p2.add(6);
        p2.add(16);
        p2.add(57);
        p2.add(132);
        p3.add(2);
        p3.add(31);
        p3.add(54);
        p3.add(101);
        tudo.add(p1);
        tudo.add(p2);
        tudo.add(p3);
        return tudo;

    }
    
    public HashMap<String, List<Integer>> dicionario(List<List<Integer>> postinglist){
        HashMap<String, List<Integer>> dict = new HashMap<>();
        List<List<Integer>> p = postinglists();
        dict.put("Brutus", p.get(0));
        dict.put("Caesar", p.get(1));
        dict.put("Calpurnia", p.get(2));
        return dict;
    }
    
    public List<Integer> search(HashMap<String, List<Integer>> di){
        List<Integer> new_list = new ArrayList<>();
        for (Integer i: di.get("Brutus")) {
            for (Integer a: di.get("Caesar")) {
                if (i==a) {
                    new_list.add(i);
                }
            }
        }
        return new_list;
    }
///A ocupar menos memoria ------------------------------
    public List<Integer> search2(HashMap<String, List<Integer>> di){
        List<Integer> new_list = new ArrayList<>();
        List<Integer> b = di.get("Brutus");
        List<Integer> c = di.get("Caesar");
        Iterator<Integer> br = b.iterator();
        Iterator<Integer> ca = c.iterator();
        Integer i = 0;
        Integer d = 0;
        br.next();
        ca.next();
        while (br.hasNext() && ca.hasNext()) {
            if (b.get(i) == c.get(d)) {
                br.next();
                ca.next();
                new_list.add(b.get(i));
                i += 1;
                d += 1;
            } else {
                if (b.get(i) > c.get(d)) {
                    d += 1;
                    ca.next();
                } else {
                    i += 1;
                    br.next();
                }
            }
        }
        return new_list;
    }
    
    //public HashMap<Integer, Integer> search_freq(List<Integer> new_list, List<List<Integer>> postinglist) {
    //    HashMap<Integer, List<Integer>> new_dict = new HashMap<>();
    //    List<List<Integer>> p = postinglists();
    //    List<Integer> st = p.get(0);
    //    List<Integer> nd = p.get(1);
    //    List<Integer> newList = new ArrayList<>();
    //    newList.addAll(st);
    //    newList.addAll(nd);
    //    for (Integer i: new_list) {
    //        int occurrences = Collections.frequency(newList, i);
    //    }
    //}
    
}

