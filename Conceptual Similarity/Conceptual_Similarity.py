<<<<<<< HEAD
import nltk as nltk
from nltk.corpus import wordnet as wn
import spacy

nlp = spacy.load('en')

def get_synsets(word):
    word_tag = nlp(word)
    for w in word_tag:
        pos = w.pos_
    if pos == 'VERB':
        pos = 'v'
    else:
        pos = 'n'
    sense = wn.synsets(word,pos)
    if sense: #se ci sono più risultati possibili
        sense = sense[0]
    print(sense)
    return sense


def find_lcs(word1, word2):
    sense1 = get_synsets(word1)
    sense2 = get_synsets(word2)
    if not sense1 or not sense2: #se wordnet non conosce la parola letta sul file
        return 0
    find = False
    parent_1_list = sense1.hypernyms()
    parent_2_list = sense2.hypernyms()
    depth_1 = 0
    depth_2 = 0
    lcs = wn.synset('entity.n.01') #lcs di default
    all_parents_1 = set()
    all_parents_2 = set()
    all_parents_1.add(sense1)
    all_parents_2.add(sense2)

    while (find == False and (parent_1_list != [] or parent_2_list != [])):  
        temp_parent_1 = []
        temp_parent_2 = []        
        for parent2 in parent_2_list:
            if (find == False):
                if (parent2 in all_parents_1):
                    lcs = parent2
                    find = True
                all_parents_2.add(parent2)
                temp_parent_2 += parent2.hypernyms()   
        for parent1 in parent_1_list:
            if (find == False):           
                if (parent1 in all_parents_2):
                    lcs = parent1
                    find = True
                all_parents_1.add(parent1)
                temp_parent_1 += parent1.hypernyms()
        parent_1_list = temp_parent_1
        parent_2_list = temp_parent_2
        depth_1 += 1

    all_parents_2 =  sense2.hypernym_paths() #carica tutti i percorsi da sense2 alla root
    paths_parents_2 = len(all_parents_2)
    depth_lcs = 0
    find = False
    i = 0

    while ( find == False ):
        while( i < paths_parents_2 and depth_lcs < len(all_parents_2[i])):
            if (all_parents_2[i][depth_lcs] == lcs):
                depth_2 = len(all_parents_2[i])
                find = True
            i += 1
        depth_lcs += 1
        i = 0

    depth_1 = depth_1 + depth_lcs
    cs = (2 * depth_lcs)/(depth_1 + depth_2)

=======
import nltk as nltk
from nltk.corpus import wordnet as wn
import spacy

nlp = spacy.load('en')

def get_synsets(word):
    word_tag = nlp(word)
    for w in word_tag:
        pos = w.pos_
    if pos == 'VERB':
        pos = 'v'
    else:
        pos = 'n'
    sense = wn.synsets(word,pos)
    if sense: #se ci sono più risultati possibili
        sense = sense[0]
    print(sense)
    return sense


def find_lcs(word1, word2):
    sense1 = get_synsets(word1)
    sense2 = get_synsets(word2)
    if not sense1 or not sense2: #se wordnet non conosce la parola letta sul file
        return 0
    find = False
    parent_1_list = sense1.hypernyms()
    parent_2_list = sense2.hypernyms()
    depth_1 = 0
    depth_2 = 0
    lcs = wn.synset('entity.n.01') #lcs di default
    all_parents_1 = set()
    all_parents_2 = set()
    all_parents_1.add(sense1)
    all_parents_2.add(sense2)

    while (find == False and (parent_1_list != [] or parent_2_list != [])):  
        temp_parent_1 = []
        temp_parent_2 = []        
        for parent2 in parent_2_list:
            if (find == False):
                if (parent2 in all_parents_1):
                    lcs = parent2
                    find = True
                all_parents_2.add(parent2)
                temp_parent_2 += parent2.hypernyms()   
        for parent1 in parent_1_list:
            if (find == False):           
                if (parent1 in all_parents_2):
                    lcs = parent1
                    find = True
                all_parents_1.add(parent1)
                temp_parent_1 += parent1.hypernyms()
        parent_1_list = temp_parent_1
        parent_2_list = temp_parent_2
        depth_1 += 1

    all_parents_2 =  sense2.hypernym_paths() #carica tutti i percorsi da sense2 alla root
    paths_parents_2 = len(all_parents_2)
    depth_lcs = 0
    find = False
    i = 0

    while ( find == False ):
        while( i < paths_parents_2 and depth_lcs < len(all_parents_2[i])):
            if (all_parents_2[i][depth_lcs] == lcs):
                depth_2 = len(all_parents_2[i])
                find = True
            i += 1
        depth_lcs += 1
        i = 0

    depth_1 = depth_1 + depth_lcs
    cs = (2 * depth_lcs)/(depth_1 + depth_2)

>>>>>>> master
    return cs