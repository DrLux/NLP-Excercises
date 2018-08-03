<<<<<<< HEAD
import requests
#print(json_data['version'])

def getkey(path = "key.txt"):
	infile = open(path, 'r')
	key = infile.read() 
	infile.close()
	return key

class babelnet:
	key = ""
	lang = ""
    
	def __init__(self,lang = "IT"):
		default_key = getkey()
		self.key = default_key
		self.lang = lang


	def getSynset(self,target, pos = "",lang = "", source = "BABELNET"):
		url = "https://babelnet.io/v5/getSynsetIds"
		if not lang:
			lang = self.lang
		payload = {'key': self.key, 'lemma': target, 'searchLang': lang.upper()}
		if pos:
			payload.update({'pos': pos.upper()})
		json_response = self.makeRequest(url,payload)
		return json_response

	def getSynsetDef(self,babelId, lang = ""):
		if not lang:
			lang = self.lang
		infos = self.getSynsetInfo(babelId,lang)
		if 'glosses' in infos:
			infos = infos['glosses']
		else:
			return None
		all_defs = []
		for elem in infos:
			if elem['language'] == lang:
				all_defs.append(elem['gloss'])
		return all_defs

	def getSynsetInfo(self,id, lang = ""):
		url = "https://babelnet.io/v5/getSynset"
		payload = {'key': self.key, 'id': id,}
		if lang:
			payload.update({'targetLang': lang.upper()})
		return self.makeRequest(url,payload)

	def makeRequest(self,url,payload):
		response = requests.get(url, params=payload)
		return response.json() 

	def getBabelId(self,target, pos = "",lang = "", source = "BABELNET"):
		info_synsets = self.getSynset(target,pos,lang,source)
		ids = []
		for syn in info_synsets:
			ids.append(syn['id'])
		return ids

	def getHypernymsIds(self,babelId):
		url = 'https://babelnet.io/v5/getOutgoingEdges'
		param = {'key': self.key, 'id': babelId}
		all_response = self.makeRequest(url,param)
		hypernyms = []
		for res in all_response:
			if res['pointer']['name'] == "Hypernym":
				hypernyms.append(res['target'])
		return hypernyms


bl = babelnet()
babelId = "bn:00034861n"
print(bl.getSynsetInfo(babelId))
'''
#hyper = bl.getHypernymsIds(babelId)
#print(bl.getSynsetDef("bn:00004146n"))
#print(getHypernyms())
#ids = bl.getBabelId("pescare")
#for babelId in ids:
#	print(babelId," = ",bl.getSynsetDef(babelId)) 
=======
import requests
#print(json_data['version'])

def getkey(path = "key.txt"):
	infile = open(path, 'r')
	key = infile.read() 
	infile.close()
	return key

class babelnet:
	key = ""
	lang = ""
    
	def __init__(self,lang = "IT"):
		default_key = getkey()
		self.key = default_key
		self.lang = lang


	def getSynset(self,target, pos = "",lang = "", source = "BABELNET"):
		url = "https://babelnet.io/v5/getSynsetIds"
		if not lang:
			lang = self.lang
		payload = {'key': self.key, 'lemma': target, 'searchLang': lang.upper()}
		if pos:
			payload.update({'pos': pos.upper()})
		json_response = self.makeRequest(url,payload)
		return json_response

	def getSynsetDef(self,babelId, lang = ""):
		if not lang:
			lang = self.lang
		infos = self.getSynsetInfo(babelId,lang)
		if 'glosses' in infos:
			infos = infos['glosses']
		else:
			return None
		all_defs = []
		for elem in infos:
			if elem['language'] == lang:
				all_defs.append(elem['gloss'])
		return all_defs

	def getSynsetInfo(self,id, lang = ""):
		url = "https://babelnet.io/v5/getSynset"
		payload = {'key': self.key, 'id': id,}
		if lang:
			payload.update({'targetLang': lang.upper()})
		return self.makeRequest(url,payload)

	def makeRequest(self,url,payload):
		response = requests.get(url, params=payload)
		return response.json() 

	def getBabelId(self,target, pos = "",lang = "", source = "BABELNET"):
		info_synsets = self.getSynset(target,pos,lang,source)
		ids = []
		for syn in info_synsets:
			ids.append(syn['id'])
		return ids

	def getHypernymsIds(self,babelId):
		url = 'https://babelnet.io/v5/getOutgoingEdges'
		param = {'key': self.key, 'id': babelId}
		all_response = self.makeRequest(url,param)
		hypernyms = []
		for res in all_response:
			if res['pointer']['name'] == "Hypernym":
				hypernyms.append(res['target'])
		return hypernyms


bl = babelnet()
babelId = "bn:00034861n"
print(bl.getSynsetInfo(babelId))
'''
#hyper = bl.getHypernymsIds(babelId)
#print(bl.getSynsetDef("bn:00004146n"))
#print(getHypernyms())
#ids = bl.getBabelId("pescare")
#for babelId in ids:
#	print(babelId," = ",bl.getSynsetDef(babelId)) 
>>>>>>> master
'''