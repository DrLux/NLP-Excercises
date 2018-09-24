
package viterbi;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 *
 * @author Luca Sorrentino
 */
public class Dictionary {
    static final Map<String, Map<String, String>> ita_to_eng; 

    static {
        Map<String, Map<String, String>> words = new LinkedHashMap<String, Map<String, String>>();
        
        Map<String, String> gli = new LinkedHashMap<String, String>();        
        gli.put("DET", "the");
        gli.put("PRON", "him");
        words.put("gli", gli);
        
        Map<String, String> ultimi = new LinkedHashMap<String, String>();                
        ultimi.put("ADJ", "last");
        words.put("ultimi", ultimi);

        Map<String, String> avanzi = new LinkedHashMap<String, String>();        
        avanzi.clear();
        avanzi.put("NOUN", "remnants");
        words.put("avanzi", avanzi);

        Map<String, String> di = new LinkedHashMap<String, String>();        
        di.put("ADP", "of");
        di.put("CCONJ", "THAN");
        words.put("di", di);
        
        Map<String, String> la = new LinkedHashMap<String, String>();        
        la.put("DET", "the");
        la.put("PRON", "her");
        words.put("la", la);
        
        Map<String, String> vecchia = new LinkedHashMap<String, String>();        
        vecchia.put("ADJ", "old");
        words.put("vecchia", vecchia);

        Map<String, String> repubblica = new LinkedHashMap<String, String>();                
        repubblica.put("PROPN", "republic");
        repubblica.put("NOUN", "republic");
        words.put("repubblica", repubblica);
        
        Map<String, String> sono = new LinkedHashMap<String, String>();        
        sono.put("VERB", "are");
        sono.put("AUX", "are");
        sono.put("AUX-AUX-VERB", "have");
        words.put("sono", sono);
        
        Map<String, String> stati = new LinkedHashMap<String, String>();        
        stati.put("NOUN", "states");
        stati.put("AUX-VERB", "been");
        stati.put("VERB", "were");
        words.put("stati", stati);
        
        Map<String, String> spazzati = new LinkedHashMap<String, String>();        
        spazzati.put("VERB", "swept");
        words.put("spazzati", spazzati);

        Map<String, String> via = new LinkedHashMap<String, String>();                
        via.put("NOUN", "way");
        via.put("ADP", "by");
        via.put("ADV", "away");
        words.put("via", via);
        
        Map<String, String> una = new LinkedHashMap<String, String>();                
        una.put("DET", "a");
        una.put("PRON", "one");
        words.put("una", una);
        
        Map<String, String> mossa = new LinkedHashMap<String, String>();                
        mossa.put("NOUN", "move");
        words.put("mossa", mossa);
        
        Map<String, String> leale = new LinkedHashMap<String, String>();                
        leale.put("ADJ", "fair");
        words.put("leale", leale);
        
        Map<String, String> ha = new LinkedHashMap<String, String>();                
        ha.put("AUX", "have");
        words.put("ha", ha);
        
        Map<String, String> ha_fatto = new LinkedHashMap<String, String>();                
        ha_fatto.put("AUX-VERB", "made");
        words.put("ha fatto", ha_fatto);
        
        Map<String, String> è = new LinkedHashMap<String, String>();                
        è.put("AUX", "is");
        words.put("è", è);
        
        Map<String, String> E = new LinkedHashMap<String, String>();                
        E.put("AUX", "is");
        words.put("E'", E);
        
        Map<String, String> e = new LinkedHashMap<String, String>();                
        e.put("AUX", "is");
        words.put("e'", e);
        
        Map<String, String> spada = new LinkedHashMap<String, String>();                
        spada.put("NOUN", "sword");
        words.put("spada", spada);
        
        Map<String, String> laser = new LinkedHashMap<String, String>();                
        laser.put("NOUN", "laser");
        words.put("laser", laser);
        
        Map<String, String> spadalaser = new LinkedHashMap<String, String>();                
        spadalaser.put("NOUN", "lightsaber");
        words.put("spadalaser", spadalaser);
        
        Map<String, String> tuo = new LinkedHashMap<String, String>();                
        tuo.put("DET", "your");
        words.put("tuo", tuo);
        
        Map<String, String> padre = new LinkedHashMap<String, String>();                
        padre.put("NOUN", "father");
        words.put("padre", padre);
        
        Map<String, String> egli = new LinkedHashMap<String, String>();                
        egli.put("NOUN", "he");
        words.put("egli", egli);
        
        Map<String, String> essa = new LinkedHashMap<String, String>();                
        egli.put("NOUN", "he");
        words.put("egli", egli);
                
        ita_to_eng = Collections.unmodifiableMap(words);
    }
}
    

