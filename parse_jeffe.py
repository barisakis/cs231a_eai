import numpy as np

in_path = "../data/jeffe_ratings.txt"
out_path = "../data/jeffe_labels.txt"

labels = ['5', '6', '7', '1', '3', '4'] # [hap, sad, sur, ang, dis, fea]

f_in = open(in_path, 'r')
f_out = open(out_path, 'w')

for line in f_in:
	data = line.strip().split(' ')
	scores = np.array([float(x) for x in data[1:-1]])
	label = labels[scores.argmax()]
	filename = data[-1].replace('-', '.') + '.' + data[0] + '.png'
	f_out.write(filename + ' ' + label + '\n')

f_out.close()
f_in.close()
