<<<<<<< HEAD
import Conceptual_Similarity as cs
from nltk.corpus import wordnet as wn
import nltk as nltk


def read_file():
    path = "pairs.txt"
    infile = open(path, 'r')
    lines = infile.readlines() #legge il file riga per riga
    infile.close()
    return lines

def write_result(log):
    outfile = open('results.txt', 'w' )
    outfile.write("Fist Word, Second word, My Conceptual Similarity, NLTK Conceptual Similarity, Error ")
    for item in log:
        outfile.write("%s\n" % item)
    outfile.write("\nGlobal error: ")
    outfile.write(str(global_error))
    outfile.close()
    

global_error = 0
local_error = 0
lines = read_file()
report = []
for line in lines:
    words = nltk.word_tokenize(line) 
    cs_value = cs.find_lcs(words[0], words[1])
    sense1 = cs.get_synsets(words[0])
    sense2 = cs.get_synsets(words[1])
    if cs_value == 0: #se la parola non esiste
        real_cs = 0
    else:
        real_cs = sense1.wup_similarity(sense2) #la funzione della libreria
    local_error = abs(cs_value - real_cs) #diff tra il mio risultato e quello ufficiale
    global_error += local_error
    report.append([sense1, sense2, round(cs_value, 2), round(real_cs, 2), round(local_error,2)]) 
=======
import Conceptual_Similarity as cs
from nltk.corpus import wordnet as wn
import nltk as nltk


def read_file():
    path = "pairs.txt"
    infile = open(path, 'r')
    lines = infile.readlines() #legge il file riga per riga
    infile.close()
    return lines

def write_result(log):
    outfile = open('results.txt', 'w' )
    outfile.write("Fist Word, Second word, My Conceptual Similarity, NLTK Conceptual Similarity, Error ")
    for item in log:
        outfile.write("%s\n" % item)
    outfile.write("\nGlobal error: ")
    outfile.write(str(global_error))
    outfile.close()
    

global_error = 0
local_error = 0
lines = read_file()
report = []
for line in lines:
    words = nltk.word_tokenize(line) 
    cs_value = cs.find_lcs(words[0], words[1])
    sense1 = cs.get_synsets(words[0])
    sense2 = cs.get_synsets(words[1])
    if cs_value == 0: #se la parola non esiste
        real_cs = 0
    else:
        real_cs = sense1.wup_similarity(sense2) #la funzione della libreria
    local_error = abs(cs_value - real_cs) #diff tra il mio risultato e quello ufficiale
    global_error += local_error
    report.append([sense1, sense2, round(cs_value, 2), round(real_cs, 2), round(local_error,2)]) 
>>>>>>> master
write_result(report) 