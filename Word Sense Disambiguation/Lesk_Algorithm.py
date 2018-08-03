import nltk
from nltk.corpus import wordnet as wn
import spacy

nlp = spacy.load('en')

LESK = 1
FIFO_LESK = 2
CS_LESK = 3

#preprocessing di una frase, elimina stopwords, punteggiatura e fa lemming
def preprocess_data(data):
	new_data = set()
	for token in data:
		if (token.is_stop == False and token.pos_ != 'PUNCT'):
			new_data.add(token.lemma_)
	return new_data

def lemming(word):
	word = nlp(word)
	for w in word:
		word = w.lemma_
	return word

def compute_cs(definition, word):
	count_context = 0
	for token in definition:
		count_context += token.similarity(word)
	count_context = count_context / len(definition)
	return count_context

def compute_overlap(sentence, definition):
	definition = preprocess_data(definition)
	overlap = len(sentence.intersection(definition)) 
	return overlap

#mapping tra i tag di spacy e quelli di wordnet
def match_pos_tag(uni_pos, wn_pos):
	if uni_pos == "NOUN":
		uni_pos = 'n'
	if uni_pos == 'VERB':
		uni_pos = 'v'
	if uni_pos == 'ADJ':
		uni_pos = 'a'
	if uni_pos == 'ADV':
		uni_pos = 'r'
	if wn_pos == 's':
		wn_pos = 'a'  
	return uni_pos == wn_pos

#filtra i possibili tag in base al pos_tag della parola target
def filter_synsets(sentence,target):
	sentence = nlp(sentence.lower()) #taggo la frase intera per essere più preciso
	target = lemming(target.lower())
	for t in sentence:
		if t.lemma_ == target: 
			pos_tag = t.pos_ 
	synsets = []
	result = []
	for ss in wn.synsets(target):
		if match_pos_tag(pos_tag,ss.pos()): #uso solo i synsets del tag di interesse
			synsets.append(ss)
	if not synsets: #se non filtro nessun synsets, li uso tutti
		synsets = wn.synsets(target) 
	return synsets,sentence,target

#di default usa il fifo_lesk
def lesk_algorithm(sentence,target,algo = 2):
	synsets,sentence,target = filter_synsets(sentence,target) 
	max_overlap = 0
	max_cs = 0
	local_overlap = 0
	local_cs = 0
	best_sense = synsets[0]
	for sense in synsets:
		definition = sense.definition().lower()
		if algo == FIFO_LESK or algo == CS_LESK:
			definition = definition.replace(target, '') #elimino la parola dalla definizione di tale parola
		definition = nlp(definition)
		local_overlap = compute_overlap(preprocess_data(sentence), definition)
		if local_overlap > max_overlap:
			max_overlap = local_overlap
			best_sense = sense
		else:
			if algo == CS_LESK:
				if local_overlap == max_overlap:
					local_cs = compute_cs(definition,nlp(target)) #in caso di pari overlap uso la content_similarity per scegliere
					if local_cs > max_cs:
						max_cs = local_cs
						best_sense = sense
	return best_sense

