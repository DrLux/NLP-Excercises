from __future__ import print_function
import nltk
import sklearn
# Import all of the scikit learn stuff
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
import pandas as pd
import warnings
from sklearn.decomposition import NMF
import math
# Suppress warnings from pandas library
warnings.filterwarnings("ignore", category=DeprecationWarning,
module="pandas", lineno=570)
import numpy
import re
import string
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import RegexpTokenizer
import collections

'''
- leggo il file
- ripulisco le frasi (stem, stop_words, punteggiatura)
- creo la matrice
- divido per due il numero di colonne
- applico la non negative matrix secomposition
- sommo tutte le colonne e ottengo un valore di score per ogni frase  
- zippo lo score alle righe originali e riordino '''

#Problemi:  tuning e non normalizzazione delle frasi lunghe

stopWords = set(stopwords.words('english')).union(set(string.punctuation))
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

def esempio():
	print("### Esempio di introduzione ###")
	example = ["Machine learning is super fun",
				"Python is super, super cool",
				"Statistics is cool, too",
				"Data science is fun",
				"Python is great for machine learning",
				"I like football",
				"Football is great to watch"]
	matrix = matrix_sentences(example)
	number_latent_concepts = 3
	W = no_negative_matrix_factorization(matrix, number_latent_concepts)
	i = 0
	columns = []
	for concept in range(0, number_latent_concepts):
		columns.append("#"+str(i+1)+" Latent Cocept")
		i += 1
	print(pd.DataFrame(W, index=example, columns = columns))
	
def read_file(path):
    infile = open(path, 'r',encoding="utf8")
    text = infile.read()
    lines = nltk.sent_tokenize(text)#split file line by line
    lines = list(filter(None, (line.rstrip() for line in lines))) #remove empty lines
    infile.close()
    return lines

def preprocess_document(document):
	processed_lines = [] #tokenize,stemming,removing stop_words and punctual of lines of documents
	for l in document:
		if len(l) > 0:
			unfiltered_words = tokenizer.tokenize(l.lower())
			temp_lines = ""			
			for word in unfiltered_words:
				if word not in stopWords and word.isalpha(): #remove stop_words and punctuation
					word = stemmer.stem(word)
					temp_lines += word+" " 	
			processed_lines.append(temp_lines)
	return processed_lines

def matrix_sentences(lines):
	vectorizer = CountVectorizer(dtype=float,min_df = 1, stop_words = 'english')
	matrix = vectorizer.fit_transform(lines)
	print(pd.DataFrame(matrix.toarray(),index=lines,columns=vectorizer.get_feature_names
	()).head(20))
	return matrix

def no_negative_matrix_factorization(matrix, number_concepts):
	model = NMF(n_components=number_concepts, init='random', random_state=0)
	W = model.fit_transform(matrix)
	return W

def calculate_score_lines(svd):
	score_sentences = svd.sum(axis=1).tolist()
	dictionary = dict(zip(score_sentences, lines))
	normalized_dictionary = dict()
	for key, value in dictionary.items():
		normalized_dictionary[key/len(value)] = value
	reordered_document = collections.OrderedDict(sorted(normalized_dictionary.items(), reverse = True))
	return reordered_document


esempio()
print("\n ### Prova pratica ### \n")
lines = read_file("../house.txt")
#processed_lines = preprocess_document(lines)
matrix = matrix_sentences(lines)
#number_latent_concepts = math.floor(matrix.getnnz()/2) #getnnz() is the new len() for sparse matrix 
number_latent_concepts = 89
svd = no_negative_matrix_factorization(matrix, number_latent_concepts)
best_lines = calculate_score_lines(svd)

print("\nRiassunto:\n")
count = 5
for key, value in best_lines.items(): 
	print("- ",value,"\n")
	count -= 1
	if (count == 0):
		break
