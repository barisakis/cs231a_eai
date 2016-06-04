import os, shutil, sys, time, re, glob
import numpy as np
import random

IMAGE_DIR_PATH = '../data/augmented_images/'
LABELS_PATH = '../data/labels.txt'

TEST_PATH = '../data/splits/test/'
TRAIN_PATH = '../data/splits/train/'
VAL_PATH = '../data/splits/val/'

TEST_SPLIT = 0.2
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.1

def loadLabels():
	d = {}
	f = open(LABELS_PATH, 'r')

	for line in f:
		data = line.strip('\n').split(' ')
		img_name = data[0]
		label = data[2]
		d[img_name] = label

	f.close()
	return d

def splitData():
	all_filenames = os.listdir(IMAGE_DIR_PATH)
	filenames = []
	for fn in all_filenames:
		if fn[0] == ".":
			continue
		filenames.append(fn)

	random.shuffle(filenames)

	test_index = int(round(len(filenames) * TEST_SPLIT))
	train_index = int(test_index + round(len(filenames) * TRAIN_SPLIT))

	test_data = filenames[:test_index]
	train_data = filenames[test_index:train_index]
	val_data = filenames[train_index:]

	return [test_data, train_data, val_data]

def writeSplit(imgs, labels, path):
	print len(imgs)
	f = open(path + 'labels.txt', 'w')

	for img_name in imgs:
		src = IMAGE_DIR_PATH + img_name
		dst = path + img_name
		shutil.copyfile(src, dst)

		out_str = img_name + " " + labels[img_name]
		f.write(out_str)

	f.close()

def writeSplits(splits, labels):
	test_data, train_data, val_data = splits
	writeSplit(test_data, labels, TEST_PATH)
	writeSplit(train_data, labels, TRAIN_PATH)
	writeSplit(val_data, labels, VAL_PATH)

def main():
	labels = loadLabels()
	splits = splitData()
	writeSplits(splits, labels)


if __name__ == "__main__":
    main()