/* Pseudocode: https://courses.engr.illinois.edu/cs447/fa2017/Slides/Lecture07.pdf
 */
package viterbi;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Luca Sorrentino
 */
public class Viterbi {
    private Map<String,Map<String,Double>> transition_dic = null; //uso double perche i fattori di una divisioni int da come output un int e poi fa il cast ma perde info
    private List emission_list = null;
    private Map<String,Integer> tag_count = null;
    private String x_set = "";
    private Map<String,Integer> emission_cache = null;
    
    public Viterbi(String set){
        this.x_set = set;
        this.transition_dic = new HashMap<String, Map<String,Double>>();
        this.emission_list = new ArrayList();
        this.tag_count = new HashMap<String, Integer>();
        this.emission_cache = new HashMap<String, Integer>();
        load_data();
    } 
    
    private void load_data(){
        String[] tokens = null;
        String key = "";
        String best_tag_per_word = "";
        List all_words = new ArrayList();
        try (BufferedReader br = new BufferedReader(new FileReader(this.x_set))) {
            String line;
            while ((line = br.readLine()) != null) {
                tokens = line.split("\\s+");
                all_words.add(tokens[0]);
                this.emission_list.add(tokens[1]);
                if (this.tag_count.containsKey(tokens[1]))
                    this.tag_count.put(tokens[1], this.tag_count.get(tokens[1])+1);
                else
                    this.tag_count.put(tokens[1], 1);
                Map<String,Double> tag_word = new HashMap<String, Double>();
                if (this.transition_dic.containsKey(tokens[0])){
                    double actual_value = 0.0;
                    tag_word = this.transition_dic.get(tokens[0]);
                    tag_word.put("total_occurrences", tag_word.get("total_occurrences")+1);
                    if (tag_word.containsKey(tokens[1])){
                        actual_value = tag_word.get(tokens[1])+1.0;
                        tag_word.put(tokens[1], actual_value);
                    } else {
                        tag_word.put(tokens[1], 1.0);
                    }
                } else {
                    tag_word.put(tokens[1], 1.0);
                    tag_word.put("total_occurrences", 1.0);
                    this.transition_dic.put(tokens[0], tag_word);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public double get_baseline(String path){
        String[] tokens = null;
        String[] bl_tags = null;
        float bl_tp = 0;
        float bl_fp = 0;
        List phrase = new ArrayList<String>();
        List correct_tags = new ArrayList<String>();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line = null;
            while ((line = br.readLine()) != null) {
                tokens = line.split("\\s+");
                if (!tokens[0].equals("#&") && !tokens[0].equals("#$")){
                    phrase.add(tokens[0]);
                    correct_tags.add(tokens[1]);
                }
                if (tokens[0].equals("#&")){
                    bl_tags = tag_baseline(phrase);
                    for (int t = 1; t < correct_tags.size(); t++){
                        if (bl_tags[t].equals(correct_tags.get(t))){
                            bl_tp += 1;
                        } else {
                            bl_fp += 1;
                        }
                    }
                phrase.clear();
                correct_tags.clear();
                }
            }
        }   catch (FileNotFoundException ex) {
            Logger.getLogger(Viterbi.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Viterbi.class.getName()).log(Level.SEVERE, null, ex);
        }
        return bl_tp/(bl_tp + bl_fp);
    }
    
    public String[] tag_baseline(List<String> phrase){
        String[] bl_tags = new String[phrase.size()];
        double tag_occurrences = 0;
        Map<String,Double> tag_word = null;
        for (int w =0; w < phrase.size(); w++){
            tag_occurrences = 0;
            if (this.transition_dic.containsKey(phrase.get(w))){
                tag_word = this.transition_dic.get(phrase.get(w));
                for (Map.Entry<String, Double> tag : tag_word.entrySet()){
                    if (!tag.getKey().equals("total_occurrences")){
                        if(tag.getValue() > tag_occurrences){
                            tag_occurrences = tag.getValue();
                            bl_tags[w] = tag.getKey();
                        }
                    }
                }
            } else {
                bl_tags[w] = "NOUN";
            }
        }
        return bl_tags;
    }

        
    public float get_precision(String path){
        String[] tokens = null;
        List correct_tags = new ArrayList<String>();
        List phrase = new ArrayList<String>();
        String[] my_tags = null;
        float tp = 0;
        float fp = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line = null;
            while ((line = br.readLine()) != null) {
                tokens = line.split("\\s+");
                if (!tokens[0].equals("#&") && !tokens[0].equals("#$")){
                    phrase.add(tokens[0]);
                    correct_tags.add(tokens[1]);
                }
                if (tokens[0].equals("#&")){
                    my_tags = viterbi(phrase);
                    for (int t = 1; t < correct_tags.size(); t++){
                        if (my_tags[t].equals(correct_tags.get(t))){
                            tp += 1;
                        } else {
                            fp += 1;
                        }
                    }
                phrase.clear();
                correct_tags.clear();
                }
            }
        }   catch (FileNotFoundException ex) {
            Logger.getLogger(Viterbi.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Viterbi.class.getName()).log(Level.SEVERE, null, ex);
        }
        return tp/(tp + fp);
    }
    
    private double get_transiction_prob(String tag_p, String tag_a){
        int count = 0;
        String key = tag_p + "_" + tag_a;
        if (this.emission_cache.containsKey(key)){
            count = this.emission_cache.get(key);
        } else {
            for (int i = 1; i < this.emission_list.size(); i++){
                if (this.emission_list.get(i).equals(tag_a) && this.emission_list.get(i-1).equals(tag_p))
                    count += 1;            
            }
            this.emission_cache.put(key, count);
        }
        return (double)count/(double)this.tag_count.get(tag_p);
    }
        
    private double get_emission_prob(String word, String tag){
        double ret  = 1.0/17.0;
        if (this.transition_dic.containsKey(word)){
            if (this.transition_dic.get(word).containsKey(tag)){
                ret = this.transition_dic.get(word).get(tag)/this.transition_dic.get(word).get("total_occurrences");
            } else{
                ret = 0.000001;
            }
                
        } else {
            if (tag.equals("NOUN") || tag.equals("VERB"))
                ret = 0.5;            
        }
        
        return ret;
    }
    
    
    public String[] viterbi(List<String> phrase){
        phrase.add("END_PHRASE");
        double e_prob = 0;
        double t_prob = 0;
        String[] state_graph = {"AUX", "PRON", "PART", "CCONJ", "PROPN", "SYM", "ADJ", "NUM", "SCONJ", "ADP", "DET", "ADV", "PUNCT", "VERB", "X", "INTJ", "NOUN"};

        double[][] viterbi = new double[phrase.size()][state_graph.length];
        int[][] backpointer = new int[phrase.size()][state_graph.length];
        for (double[] row : viterbi) {
           Arrays.fill(row, 0.0);
        }
        double new_score = 0.0;
        
        for (int t = 0; t < state_graph.length; t++){
            t_prob = this.get_transiction_prob("START", state_graph[t]);
            e_prob = this.get_emission_prob(phrase.get(0), state_graph[t]);
            new_score = t_prob * e_prob;
            if (new_score > viterbi[0][t]){
                viterbi[0][t] = new_score;    
            } 
        }
        
        //corpo centrale
        for (int w = 1; w < phrase.size(); w++){
            for (int t = 0; t < state_graph.length; t++){
                viterbi[w][t] = 0.0;
                for (int t_p = 0; t_p < state_graph.length; t_p++){
                    t_prob = this.get_transiction_prob(state_graph[t_p], state_graph[t]);
                    new_score = viterbi[w-1][t_p] * t_prob;
                    if (new_score > viterbi[w][t]){
                        viterbi[w][t] = new_score;
                        backpointer[w][t] = t_p;
                    }
                    new_score = 0;
                }
                e_prob = this.get_emission_prob(phrase.get(w), state_graph[t]);
                viterbi[w][t] = viterbi[w][t] * e_prob;
            }
        }
        int w = phrase.size()-2;
        int t_max = backpointer[phrase.size()-1][0];;
                    
        String[] tags = new String[phrase.size()];
        while (w >= 0){
            tags[w] = state_graph[t_max];
            t_max = backpointer[w][t_max];
            w--;
        }  
        return tags;
    }    
    
    public List<String> preprocess_input(String original_phrase){
        String phrase[] = original_phrase.split("\\s+");
        List processed_phrase = new ArrayList<String>();
        for (int t = 0; t < phrase.length; t++){
            switch(phrase[t]){
                case "del":
                    processed_phrase.add("di");
                    processed_phrase.add("il");
                    break;
                case "dello":
                    processed_phrase.add("di");
                    processed_phrase.add("lo");
                    break;
                case "della":
                    processed_phrase.add("di");
                    processed_phrase.add("la");
                    break;
                case "dei":
                    processed_phrase.add("di");
                    processed_phrase.add("i");
                    break;
                case "degli":
                    processed_phrase.add("di");
                    processed_phrase.add("gli");
                    break;
                case "delle":
                    processed_phrase.add("di");
                    processed_phrase.add("le");
                    break;
                case "al":
                    processed_phrase.add("a");
                    processed_phrase.add("al");
                    break;
                case "allo":
                    processed_phrase.add("a");
                    processed_phrase.add("lo");
                    break;
                case "alla":
                    processed_phrase.add("a");
                    processed_phrase.add("la");
                    break;
                case "ai":
                    processed_phrase.add("a");
                    processed_phrase.add("i");
                    break;
                case "agli":
                    processed_phrase.add("a");
                    processed_phrase.add("gli");
                    break;
                case "alle":
                    processed_phrase.add("a");
                    processed_phrase.add("le");
                    break;
                case "dal":
                    processed_phrase.add("da");
                    processed_phrase.add("il");
                    break;
                case "dallo":
                    processed_phrase.add("da");
                    processed_phrase.add("lo");
                    break;
                case "dalla":
                    processed_phrase.add("da");
                    processed_phrase.add("la");
                    break;
                case "dai":
                    processed_phrase.add("da");
                    processed_phrase.add("i");
                    break;
                case "dagli":
                    processed_phrase.add("da");
                    processed_phrase.add("gli");
                    break;
                case "dalle":
                    processed_phrase.add("da");
                    processed_phrase.add("le");
                    break;
                case "nel":
                    processed_phrase.add("in");
                    processed_phrase.add("il");
                    break;
                case "nello":
                    processed_phrase.add("in");
                    processed_phrase.add("lo");
                    break;
                case "nella":
                    processed_phrase.add("in");
                    processed_phrase.add("la");
                    break;
                case "nei":
                    processed_phrase.add("in");
                    processed_phrase.add("i");
                    break;
                case "negli":
                    processed_phrase.add("in");
                    processed_phrase.add("gli");
                    break;
                case "nelle":
                    processed_phrase.add("in");
                    processed_phrase.add("le");
                    break;
                case "col":
                    processed_phrase.add("con");
                    processed_phrase.add("il");
                    break;
                case "coi":
                    processed_phrase.add("com");
                    processed_phrase.add("i");
                    break;
                case "sul":
                    processed_phrase.add("su");
                    processed_phrase.add("il");
                    break;
                case "sullo":
                    processed_phrase.add("su");
                    processed_phrase.add("lo");
                    break;
                case "sulla":
                    processed_phrase.add("su");
                    processed_phrase.add("la");
                    break;
                case "sui":
                    processed_phrase.add("su");
                    processed_phrase.add("i");
                    break;
                case "sugli":
                    processed_phrase.add("su");
                    processed_phrase.add("gli");
                    break;
                case "sulle":
                    processed_phrase.add("su");
                    processed_phrase.add("le");
                    break;
                default:
                    processed_phrase.add(phrase[t]);
            }
        }
        return processed_phrase;
    }
		
}
		