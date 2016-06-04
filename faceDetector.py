import os, shutil, sys, time, re, glob
import numpy as np
import cv2

CASCADE_PATH = '/Users/barisakis/opencv/data/haarcascades/haarcascade_frontalface_default.xml'
IN_PATH = '../data/images/'
OUT_PATH = '../data/cropped_images/'
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)

filenames = os.listdir(IN_PATH)
for filename in filenames:

	# Read the image
	image = cv2.imread(IN_PATH + filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = FACE_CASCADE.detectMultiScale(
	    gray,
	    scaleFactor=1.1, # increase to reduce false positives
	    minNeighbors=5,
	    minSize=(30, 30),
	)

	# If no faces found, skip image
	if len(faces) == 0:
		continue

	# Find largest face
	faces.tolist().sort( lambda f1, f2: int(f1[2] * f1[3]) - int(f2[2] * f2[3]) )
	face = faces[0]

	# Crop and save image
	(x, y, w, h) = face
	cropped_img = image[y:(y+h), x:(x+h)]
	cv2.imwrite(OUT_PATH + filename, cropped_img)

	"""
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
		img = image[y:(y+h), x:(x+h)]
		cv2.imshow("Cropped found" ,img)
		cropped_path = "./c_images/" + "cropped_" + img_path
		print cropped_path
		# cv2.imwrite('cropped_test.png', img)

	cv2.imshow("Faces found" ,image)
	cv2.waitKey(0)
	"""







