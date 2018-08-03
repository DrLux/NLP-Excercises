from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
import operator
from nltk.corpus import stopwords
import string
import math
import collections


stopWords = set(stopwords.words('english')).union(set(string.punctuation))
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

def load_nasari(path): #nasari = dict{lemma, {[relate_word, score], [relate_word_2, score_2]}}
	infile = open(path, 'r', encoding="utf8")
	lines = infile.readlines() #legge il file riga per riga
	nasari = dict()
	for line in lines:
		line = line.lower().rstrip().split(";")
		vector = dict()
		for i in range( 2, len(line)):
			text = line[i].split("_")
			if (len(text) == 2):
				vector[text[0]] = text[1]
		nasari[line[1]] = vector
	infile.close()
	return nasari

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
	hyperparameter_title = 1.5
	for word in title:
		value = keywords[word]
		keywords[word] = value * hyperparameter_title 

def compute_overlap(tokenized_sting1,tokenized_sting2,keywords,nasari):
	line1 = set(tokenized_sting1)
	line2 = set(tokenized_sting2)
	words_value = 0
	for w1 in line1:
		for w2 in line2:
			words_value += compare_nasari(nasari,w1,w2)
	common_words = line1.intersection(line2)
	for word in common_words:
		words_value += keywords[word]
	words_value = words_value / (math.log(len(line1))+math.log(len(line2)))
	return words_value


def compare_nasari(nasari,w1,w2):
	v1 = nasari.get(w1)
	v2 = nasari.get(w2)
	counter = 0.0
	if (v1 != None and v2 != None):
		common_words = set(v1.keys()).intersection(set(v2.keys()))
		for word in common_words:
			counter += float(v1[word]) + float(v2[word])
	return counter

def evaluate_cohesion(lines,keywords,nasari):	
	n = len(lines)
	score_lines = dict() #dictionary containing {index_of_lines : score}
	for idx1 in range( 0, n-1): 
		for idx2 in range( idx1+1, n):
			score = compute_overlap(lines[idx1],lines[idx2],keywords,nasari)
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
	return list(reordered_lines.values())

document = read_file("../house.txt")
lines,keywords = preprocess_document(document)
prioritize_title(lines[0],keywords)
nasari = load_nasari("nasari_small.txt")
score_lines = evaluate_cohesion(lines,keywords,nasari)
best_lines = extract_best_lines(score_lines,document)
summarizing_factors = math.floor((70 * len(lines)) / 100.0)
for i in range( 0, 5):
	print("\n",best_lines[i])
