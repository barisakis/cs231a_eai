import os, shutil, sys, time, re, glob
import numpy as np
import cv2

IN_PATH = '../data/cropped_images/'
OUT_PATH = '../data/augmented_images/'

IMG_SIZE = (250, 250)


filenames = os.listdir(IN_PATH)
for filename in filenames:

	# Skip random files in directory
	if filename[0] == ".":
		continue

	# Read the image into grayscale
	img = cv2.imread(IN_PATH + filename, 0)

	# Resize image to IMG_SIZE
	img = cv2.resize(img, IMG_SIZE)

	# Save image
	cv2.imwrite(OUT_PATH + filename, img)
