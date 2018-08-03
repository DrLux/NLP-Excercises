<<<<<<< HEAD
import nltk
import Ext_Lesk_Algorithm as la


def read_file(path = "inputs.txt"):
    infile = open(path, 'r')
    lines = infile.readlines() #legge il file riga per riga
    infile.close()
    return lines

def write_result(file, lesk,ext_lesk, sentence, word): 
	file.write("\nFrase: " + sentence + "\n")
	file.write("\n\tDisambiguazione di '"+word+"' con lesk: " + lesk + "\n")
	file.write("\n\tDisambiguazione di '"+word+"' con extended lesk: " + ext_lesk + "\n")

lines = read_file()
with open("results.txt", "w") as f:
	for line in lines:
		input = line.split('|')
		sentence = input[0].strip()
		word = input[1].strip()
		lesk = la.lesk_algorithm(sentence,word,1)
		ext_lesk = la.lesk_algorithm(sentence,word,2)
		write_result(f,lesk,ext_lesk,sentence,word)
f.close()

'''
#sentence = input('Enter the Sentence: ')
#word = input('Enter the Word: ')
sentence = "amo andare a cavallo, ogni mattino, nel parco."
word = 'cavallo'
sense = la.lesk_algorithm(sentence,word,2)
#nltk_lesk_sense = lesk(nltk.word_tokenize(sentence), word)
if not sense:
	print("Nessun risultato utile trovato")
=======
import nltk
import Ext_Lesk_Algorithm as la


def read_file(path = "inputs.txt"):
    infile = open(path, 'r')
    lines = infile.readlines() #legge il file riga per riga
    infile.close()
    return lines

def write_result(file, lesk,ext_lesk, sentence, word): 
	file.write("\nFrase: " + sentence + "\n")
	file.write("\n\tDisambiguazione di '"+word+"' con lesk: " + lesk + "\n")
	file.write("\n\tDisambiguazione di '"+word+"' con extended lesk: " + ext_lesk + "\n")

lines = read_file()
with open("results.txt", "w") as f:
	for line in lines:
		input = line.split('|')
		sentence = input[0].strip()
		word = input[1].strip()
		lesk = la.lesk_algorithm(sentence,word,1)
		ext_lesk = la.lesk_algorithm(sentence,word,2)
		write_result(f,lesk,ext_lesk,sentence,word)
f.close()

'''
#sentence = input('Enter the Sentence: ')
#word = input('Enter the Word: ')
sentence = "amo andare a cavallo, ogni mattino, nel parco."
word = 'cavallo'
sense = la.lesk_algorithm(sentence,word,2)
#nltk_lesk_sense = lesk(nltk.word_tokenize(sentence), word)
if not sense:
	print("Nessun risultato utile trovato")
>>>>>>> master
'''