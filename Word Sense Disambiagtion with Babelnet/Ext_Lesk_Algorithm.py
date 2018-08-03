<<<<<<< HEAD
import nltk
import babelnet
import spacy

nlp = spacy.load('it')
bl = babelnet.babelnet()

#preprocessing di una frase, elimina stopwords, punteggiatura e fa lemming
def preprocess_data(data):
	new_data = set()
	for token in data:
		if (token.is_stop == False and token.pos_ != 'PUNCT'):
			new_data.add(token.lemma_)
	return new_data

def compute_overlap(sentence, definition):
	definition = preprocess_data(definition)
	overlap = len(sentence.intersection(definition))
	return overlap


#filtra i possibili tag in base al pos_tag della parola target
def getFiltredBabelId(sentence,target):
	sentence = nlp(sentence.lower())
	target = target.lower()
	for w in sentence:
		if w.text == target: 
			pos_tag = w.pos_ 
	babelIDs = bl.getBabelId(target, pos_tag)
	if not babelIDs: 
		babelIDs = bl.getBabelId(target)
	return babelIDs,sentence,target

#di default usa il fifo_lesk
def lesk_algorithm(sentence,target, algo):
	babelIDs,sentence,target = getFiltredBabelId(sentence,target) 
	max_overlap = 0
	local_overlap = 0
	max_cs = 0
	local_cs = 0
	definition = set()
	best_sense = None
	for bid in babelIDs:
		definition = bl.getSynsetDef(bid)
		if len(definition) > 0:
			definition = definition[0]
			if algo == 2:
				hypernyms = bl.getSynsetDef(bl.getHypernymsIds(bid))
				if hypernyms:
					for hype in hypernyms:
						definition = definition+' '+hype
			definition = nlp(definition)
			local_overlap = compute_overlap(preprocess_data(sentence), definition)
			if local_overlap > max_overlap:
				max_overlap = local_overlap
				best_sense = definition.text
	if not best_sense:
		best_sense = definition.text

=======
import nltk
import babelnet
import spacy

nlp = spacy.load('it')
bl = babelnet.babelnet()

#preprocessing di una frase, elimina stopwords, punteggiatura e fa lemming
def preprocess_data(data):
	new_data = set()
	for token in data:
		if (token.is_stop == False and token.pos_ != 'PUNCT'):
			new_data.add(token.lemma_)
	return new_data

def compute_overlap(sentence, definition):
	definition = preprocess_data(definition)
	overlap = len(sentence.intersection(definition))
	return overlap


#filtra i possibili tag in base al pos_tag della parola target
def getFiltredBabelId(sentence,target):
	sentence = nlp(sentence.lower())
	target = target.lower()
	for w in sentence:
		if w.text == target: 
			pos_tag = w.pos_ 
	babelIDs = bl.getBabelId(target, pos_tag)
	if not babelIDs: 
		babelIDs = bl.getBabelId(target)
	return babelIDs,sentence,target

#di default usa il fifo_lesk
def lesk_algorithm(sentence,target, algo):
	babelIDs,sentence,target = getFiltredBabelId(sentence,target) 
	max_overlap = 0
	local_overlap = 0
	max_cs = 0
	local_cs = 0
	definition = set()
	best_sense = None
	for bid in babelIDs:
		definition = bl.getSynsetDef(bid)
		if len(definition) > 0:
			definition = definition[0]
			if algo == 2:
				hypernyms = bl.getSynsetDef(bl.getHypernymsIds(bid))
				if hypernyms:
					for hype in hypernyms:
						definition = definition+' '+hype
			definition = nlp(definition)
			local_overlap = compute_overlap(preprocess_data(sentence), definition)
			if local_overlap > max_overlap:
				max_overlap = local_overlap
				best_sense = definition.text
	if not best_sense:
		best_sense = definition.text

>>>>>>> master
	return best_sense