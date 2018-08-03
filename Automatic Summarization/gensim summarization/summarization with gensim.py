import gensim
from gensim.summarization.summarizer import summarize
import nltk

def read_file(path):
    infile = open(path, 'r',encoding="utf8")
    text = infile.read()
    infile.close()
    return text

summarization = summarize(read_file("../house.txt"), 0.2)
best_lines = nltk.sent_tokenize(summarization)
for i in range( 0, 5):
	print("\n",best_lines[i])
