#coding=utf-8
#Roger Ventura Castelló
#173823
#CILN


def readAndCountData(file):
	#Donat un fitxer de training set,  retorna en una llista les paraules
	#amb els seus tags i amb el número d'ocurrencies d'aquestes.

	countline = {}

	for line in file:
		line = line.decode("latin_1").encode("UTF-8")
		if line not in countline:
			countline[line] = 1
		else:
			countline[line] += 1

	getmax = {}
	data = []
	
	for key in countline:
		getmax[key] = float("-Inf")
		
	for ke in countline:
		if countline[key] >= getmax[key]:
			getmax[key] = countline[key]

	for k in getmax:
		words = k.split("\t")
		words[1] = words[1].replace("\n" , "")
		words.append(getmax[k])
		data.append(words)

	return data


def writeDataWithOcurrences(data, newfile):
	#Donat una llista amb paraules + tag + ocurrencies, les escriu en un fitxer

	for tup in data:
		words = str(tup[0] + "\t" + tup[1] + "\t" + str(tup[2]) + "\n")
		words.decode("UTF-8").encode('latin-1')
		newfile.write(words)


def readModelData(model):
	# llegeix el model del training set, el qual conté tant la paraula com el tag com el número de ocurrencies
	tup_values = []

	for line in model:
		line = line.decode("latin_1").encode("UTF-8")
		tup = line.split("\t")
		tup_values.append(tup)

	return tup_values


def readAssignedTagsAndWrite(data, testfile, outfile):
	#donat una llista (data) amb els valors de el model de training set, la utilitza per
	#seleccionar el tag més comú per les paraules de el testfile, i escriu tant la paraula com el seu tag al outfile

	final_tag = {}
	aux_values = {}
	for line in testfile:
		line = line.decode("latin_1").encode("UTF-8")
		line = line.replace("\n" , "")
		aux_values[line] = -1

		for word in data:
			if line == word[0] and word[2] >= aux_values[line]:
				aux_values[line] = word[2]
				final_tag[line] = word[1]

		if line not in final_tag: #En cas de que la paraula no aparegui al training set
			final_tag[line] = "NP" #Li assignarem el tag de nom propi, ja que solen ser les que menys apareixen al training set
	

	for key in final_tag:
		words = str(key + "\t" + final_tag[key] + "\n")
		words.decode("UTF-8").encode('latin-1')
		
		outfile.write(words)

def extractData(file):
	#retorna una llista amb les paraules y tags del fitxer donat.
	data = [] 

	for line in file:
		line.split("\t")
		data.append(line)

	return data


def compareOutputs(golddata, testdata):
	#compara dos llistes per saber els valors iguals

	equal = set(golddata) & set(testdata)
	print len(golddata) , len(testdata), len(equal)
	return (len(equal)/len(testdata))

	
"""
Executar els 3 exerecicis alhora dura aproximadament 90 segons.
"""


#Exercici 1

data = []
file = open("corpus.txt" , "r")
newfile = open("lexic.txt" , "w")

data = readAndCountData(file)
writeDataWithOcurrences(data, newfile)

file.close()
newfile.close()



#Exercici 2

data = []
model = open("lexic.txt", "r")
test1 = open("test_1.txt" , "r")
test2 = open("test_2.txt", "r")
test1_sol = open("test_1_sol.txt" , "w")
test2_sol = open("test_2_sol.txt" , "w")

data = readModelData(model)
readAssignedTagsAndWrite(data ,test1 ,test1_sol)
readAssignedTagsAndWrite(data ,test2 ,test2_sol)


model.close()
test1.close()
test1_sol.close()


#Exercici 3


test1_sol = open("test_1_sol.txt" , "r")
test2_sol = open("test_2_sol.txt" , "r")
gold1_sol = open("gold_standard_1.txt" , "r")
gold2_sol = open("gold_standard_2.txt" , "r")

accuracy1 = compareOutputs(extractData(gold1_sol) , extractData(test1_sol))
print "Accuracy for test1 solution: " + str(accuracy1)

accuracy2 = compareOutputs(extractData(gold2_sol) , extractData(test2_sol))
print "Accuracy for test2 solution: " + str(accuracy2)

test1_sol.close()
test2_sol.close()
gold1_sol.close()
gold2_sol.close()