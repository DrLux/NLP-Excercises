from gensim.summarization.summarizer import summarize
from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import logging, gensim
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
import string
from gensim.models.tfidfmodel import TfidfModel

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

text = read_file("house.txt")
tokenized_text = []
filtered_line = []
for line in text:
	if len(line) > 0:
		line = nltk.word_tokenize(line.lower())
		for token in line:
			if token not in stopWords and token.isalpha():
				filtered_line.append(token)
		tokenized_text.append(filtered_line)

id2word = gensim.corpora.Dictionary(tokenized_text)
corpus = [id2word.doc2bow(doc) for doc in tokenized_text]

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=5, update_every=1, chunksize=10000, passes=1)
num_topics = lda.num_topics
topicWordProbMat = lda.print_topics(num_topics)
print(topicWordProbMat[0])