import os

LABEL_PATH = '../data/splits/test/labels.txt'

f = open(LABEL_PATH, 'r')
counts = {}
total = 0.0
for line in f:
	data = line.strip('\n').split(' ')
	label = data[1]
	if label in counts:
		counts[label] += 1
	else:
		counts[label] = 1
	total += 1

for key in counts.keys():
	print (key, counts[key], counts[key]/total )