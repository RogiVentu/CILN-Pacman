
data = []
file = open("corpus.txt" , "r")

for line in file:
	line.rstrip("\n")
	tup = line.split("\t")
	data.append(tup)

#print data[0] , data[1]
#first5lines = file.readlines()[0:5] #


file.close()