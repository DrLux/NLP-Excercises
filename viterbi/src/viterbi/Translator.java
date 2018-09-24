/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package viterbi;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Luca Sorrentino
 */
public class Translator {
     
    public static void main(String[] args) {
        Translator t = new Translator();
        Viterbi v = new Viterbi("files/combined_train_set.txt");
        t.print_baseline(v);
        t.print_precision(v);
        String  phrase = "E' la spada laser di tuo padre";
        t.load_phrase(phrase, v, t);
        phrase = "Ha fatto una mossa leale";
        t.load_phrase(phrase, v, t);
        phrase = "Gli ultimi avanzi della vecchia Repubblica sono stati spazzati via";
        t.load_phrase(phrase, v, t);
       

    } 
    
    public void load_phrase(String phrase, Viterbi v, Translator t){
        List processed_phrase = v.preprocess_input(phrase);
        String[] tagged_phrase = t.tag_phrase(v, processed_phrase);
        t.translate(processed_phrase, tagged_phrase);
    }
    
    public void print_baseline(Viterbi v){
        System.out.println("Calcolo della Baseline!");        
        long startTime = System.currentTimeMillis();
        System.out.println("Baseline: " + v.get_baseline("files/normal_test_set.txt")*100.0 +"%");        
        long endTime = System.currentTimeMillis();
        long duration = (endTime - startTime);
        System.out.println("Tempo di computazione: "+ duration/1000.0 + " secondi. \n");
    }
    
    public void print_precision(Viterbi v){
        System.out.println("Calcolo del livello di precisione del modello!");        
        long startTime = System.currentTimeMillis();
        System.out.println("Precision: " + v.get_precision("files/normal_test_set.txt")*100.0 +"%");                
        long endTime = System.currentTimeMillis();
        long duration = (endTime - startTime);
        System.out.println("Tempo di computazione: "+ duration/1000.0 + " secondi. \n");
    }
    
    public String[] tag_phrase(Viterbi v, List phrase){
        System.out.println("Tagging della frase con Viterbi!");        
        System.out.println("Frase in input: "+ phrase+"\n");
        long startTime = System.currentTimeMillis();
        String[] pos_tags = v.viterbi(phrase);
        long endTime = System.currentTimeMillis();
        long duration = (endTime - startTime);
        for (int t = 0; t < pos_tags.length -1; t++){
            System.out.println(phrase.get(t) + " -> " + pos_tags[t] + "\n");            
        }
        System.out.println("Tempo di computazione: "+ duration/1000.0 + " secondi. \n");
        return pos_tags;
    }
    
    public void translate(List phrase, String[] tags){
        Dictionary dict = new Dictionary();
        String word = "";
        List<String> trasleted_words = new ArrayList();
        List<String> new_tags = new ArrayList<>();
        List<String> final_phrase = new ArrayList();
        
        for (int i = 0; i < tags.length-1; i++){
            word = ((String)phrase.get(i)).toLowerCase();
            if (tags[i].equals("AUX") && tags[i+1].equals("AUX") && tags[i+2].equals("VERB")){
                tags[i] = "AUX-AUX-VERB";
                tags[i+1] = "AUX-VERB";
            } else {
                if (word.equals("ha") && ((String)phrase.get(i+1)).toLowerCase().equals("fatto")){
                    i = i+1;
                    tags[i] = "AUX-VERB";
                    word = "ha fatto";
                }
                if (word.equals("spada") && ((String)phrase.get(i+1)).toLowerCase().equals("laser")){
                    i = i+1;
                    word = "spadalaser";
                }
            }            
            trasleted_words.add(dict.ita_to_eng.get(word).get(tags[i]));
            new_tags.add(tags[i]);
            
        }
        System.out.println("\nTraduzione intermedia:\n" + trasleted_words.toString());
        
        //RIODINAMENTO        
        for (int i = 0; i < trasleted_words.size(); i++) {
            word = trasleted_words.get(i);  
            if (word.equals("is"))
                final_phrase.add("it");
            if (word.equals("made"))
                final_phrase.add("he");
            if (i < trasleted_words.size()-1 && new_tags.get(i).equals("NOUN") && new_tags.get(i+1).equals("ADJ")){
                final_phrase.add(trasleted_words.get(i+1));
                i++;
            }
            final_phrase.add(word);
        }
        System.out.println("\nTraduzione finale:\n"+ final_phrase+"\n");
    }
    
}
