Spiegare cosa fa questo esercizio e cosa contengono i txt

appunti: 
1 Le parole che wordnet non riconosce le considero a Cs = 0 
2 L' LCS di default è la radice ( wn.synset('entity.n.01') ) 
3 La complessità della ricerca di LCS = O(p1 + p2 + dist) dove: p1 = numero di genitori del sense1, p2 = numero di genitori del sense2, dist = distanza tra uno dei due sense e l' lcs 