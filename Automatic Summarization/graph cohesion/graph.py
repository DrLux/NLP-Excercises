from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
import operator
from nltk.corpus import stopwords
import math
import string
import collections

'''
- leggo il file
- ottengo un array di righe preprocessate (stem + stowords + punctual)
- ottengo una lista keywords = {parola : frequenza}
- incremento la frequenza/priorità (di un fattore moltiplicativo N) delle parole che sono presenti anche nel titolo
- elaboro tutte le coppie di righe e ne calcolo il valore di coesione (non solo quante parole in comune ma anche il valore delle stesse) e dividendo il risultato per la lunghezza delle righe. In questo modo 
creo un dizionario score_lines = 
{punteggio riga : indice riga}
- ordino score_line per gli score e uso l' indice per riprendere le righe originali del documento di testo e creo best_lines '''

stopWords = set(stopwords.words('english')).union(set(string.punctuation))
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')


def read_file(path):
    infile = open(path, 'r',encoding="utf8")
    text = infile.read()
    lines = sent_tokenize(text)#split file line by line
    lines = list(filter(None, (line.rstrip() for line in lines))) #remove empty lines
    infile.close()
    return lines

def preprocess_document(document):
	keyword_value = 0 #count frequency of the word
	keywords = dict() #dictionary {word:value}
	processed_lines = [] #tokenize,stemming,removing stop_words and punctual of lines of documents
	for l in document:
		if len(l) > 0:
			unfiltered_words = tokenizer.tokenize(l.lower())
			temp_lines = []			
			for word in unfiltered_words:
				if word not in stopWords and word.isalpha(): #remove stop_words and punctuation
					word = stemmer.stem(word)
					temp_lines.append(word)
					keyword_value = 1
					if word in keywords:
						keyword_value = keywords[word] + 1
					keywords[word] = keyword_value 	
			processed_lines.append(temp_lines)
	return processed_lines, keywords
	
def prioritize_title(title,keywords):
	hyperparameter_title = 1.15
	for word in title:
		value = keywords[word]
		keywords[word] = value * hyperparameter_title 

def compute_overlap(tokenized_sting1,tokenized_sting2,keywords):
	line1 = set(tokenized_sting1)
	line2 = set(tokenized_sting2)
	words_value = 0
	common_words = line1.intersection(line2)
	for word in common_words:
		words_value += keywords[word]
	words_value = words_value / (math.log(len(line1))+math.log(len(line2)))
	return words_value

def evaluate_cohesion(lines,keywords):	
	n = len(lines)
	score_lines = dict() #dictionary containing {index_of_lines : score}
	for idx1 in range( 0, n-1): 
		for idx2 in range( idx1+1, n):
			score = compute_overlap(lines[idx1],lines[idx2],keywords)
			if idx1 in score_lines: #ogni valore di score che trovo lo inserisco in entrambe le frasi confrontate
				score_lines[idx1] += score	
			else: 
				score_lines[idx1] = score
			if idx2 in score_lines:
				score_lines[idx2] += score	
			else: 
				score_lines[idx2] = score
	return score_lines

def extract_best_lines(score_lines,lines):
	best_scores = list(score_lines.values())
	dictionary = dict(zip(best_scores, lines))
	reordered_lines = collections.OrderedDict(sorted(dictionary.items(), reverse = True))
	return reordered_lines

document = read_file("../house.txt")
lines,keywords = preprocess_document(document)
prioritize_title(lines[0],keywords)
score_lines = evaluate_cohesion(lines,keywords)
best_lines = extract_best_lines(score_lines,document)
print("\nRiassunto:\n")
count = 5
for key, value in best_lines.items(): 
	print("- ",value,"\n")
	count -= 1
	if (count == 0):
		break
