import re, string, os

def cleanText(file):
	#Donat un fitxer, borrem tots els digits, puntuacions, caracters no ASCII, 
	#cambiem tot a minuscula i reemplacem dos espais per un
	clean_str = ""

	for line in file:
		line = line.lower()
		line = line.translate(None, string.punctuation)
		line = line.translate(None, string.digits)
		line = line.translate(None, '\xe2\x80\x94')
		line = line.replace("  ", " ")

		clean_str += line

	return clean_str

def getOcurrencesText(text):
	#Retornem el numero de vegades que apareix cada paraula en text
	data = {}

	words = text.split(" ")
	for w in words:
		if w in data:
			data[w] += 1
		else:
			data[w] = 1

	return data

def getNMostUsedWords(data, N):
	#Obtenim de data, les N paraules que tenen mes ocurrencies
	aux_n = 0
	n_words = []

	while aux_n < N:
		aux_max = float("-Inf")	
		for key in data:
			if data[key] > aux_max and key not in n_words:
				aux_max = data[key]
				aux_word = key
		n_words.append(aux_word)
		aux_n += 1

	return n_words


def NWordsforAllFiles(N):

 	text = ""

 	for filename in os.listdir("dataset/"):
 		file = open("dataset/" + filename)
 		text += cleanText(file)
 		file.close()

 	data = getOcurrencesText(text)
 	n_words = getNMostUsedWords(data, N)
 	
 	return n_words



N = 5
print NWordsforAllFiles(N)
'''
wordsSum = {}

file = open("dataset/1_female")
text = cleanText(file)
res = getOcurrencesText(wordsSum, text)
nw = getNMostUsedWords(res, 5) #
print nw

file.close()
'''
