import nltk
import Lesk_Algorithm as la
from nltk.wsd import lesk


def read_file(path = "inputs.txt"):
    infile = open(path, 'r')
    lines = infile.readlines() #legge il file riga per riga
    infile.close()
    return lines

def write_result(file, mylesk,fifo_lesk,cs_lesk, nltk_sense, sentence, word): 
	file.write("Sentence: " + sentence + " -> Word: " + word + "\n")
	file.write("\n\tMy Lesk: " + mylesk.definition() + " (" + str(mylesk) +") \n")
	file.write("\n\tFifo Lesk: " + fifo_lesk.definition() + " (" + str(fifo_lesk) +") \n")
	file.write("\n\tMy CS Lesk: " + cs_lesk.definition() + " (" + str(cs_lesk) +") \n")
	file.write("\n\tWordnet Library Lesk: " + nltk_sense.definition() + " (" + str(nltk_sense) +")\n\n")


lines = read_file()
with open("results.txt", "w") as f:
	for line in lines:
		input = line.split('|')
		sentence = input[0].strip()
		word = input[1].strip()
		mylesk = la.lesk_algorithm(sentence,word,1)
		fifo_lesk = la.lesk_algorithm(sentence,word,2)
		cs_lesk = la.lesk_algorithm(sentence,word,3)
		nltk_lesk_sense = lesk(nltk.word_tokenize(sentence), word)
		write_result(f,mylesk,fifo_lesk,cs_lesk,nltk_lesk_sense,sentence,word)
f.close()

'''
#sentence = input('Enter the sentence: ')
#word = input('Enter the word: ')
sentence = 'Germany sells arms to Saudi Arabia.'
word = 'arms'
sense = la.lesk_algorithm(sentence,word,2)
nltk_lesk_sense = lesk(nltk.word_tokenize(sentence), word)
if not sense:
	print("Nessun risultato utile trovato")
else:	
	print(sentence)
	print("My results: ", sense, sense.definition())
	print("Nltk results: ", nltk_lesk_sense, nltk_lesk_sense.definition())
'''