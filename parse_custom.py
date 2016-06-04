import os
from PIL import Image

DIR = '../data/custom_images/'
NAMES = ['Tanner', 'Baris', 'Katie']

OUT_LABELS = '../data/custom_images/labels.txt'
OUT_IMAGES = '../data/custom_images/all_images/'

f_out = open(OUT_LABELS, 'w')
for name in NAMES:
	f_labels = open(DIR + name + "/labels.txt", 'r')
	for i, line in enumerate(f_labels):
		(fn, label) = line.strip().split(' ')
		im = Image.open(DIR + name + "/" + fn)

		new_fn = name + "_" + str(i) + ".png"
		im.save(OUT_IMAGES + new_fn, 'png')
		f_out.write(new_fn + " " + label + "\n")

f_out.close()

