import os
import shutil
from PIL import Image, ImageOps

ROOT = "../data"

IMAGE_IN = "raw_images"
IMAGE_OUT = "images"

LABEL_IN = "raw_labels"
LABEL_OUT = "labels"

NUM_IMAGES = 3

def reformat_data():
	# File for writing labels
	label_out_path = ('/').join([ROOT, LABEL_OUT, "labels.txt"])
	f = open(label_out_path, 'w')

	path1 = ROOT + "/" + IMAGE_IN
	dirs = os.listdir(path1)
	for i, dirname1 in enumerate(dirs):

		path2 = path1 + "/" + dirname1
		for dirname2 in os.listdir(path2):
			if dirname2[0] == ".":
				continue

			path3 = path2 + "/" + dirname2
			image_filenames = os.listdir(path3)

			if len(image_filenames) < 3:
				continue

			label_path = ("/").join([ROOT, LABEL_IN, dirname1, dirname2])

			# Try to get the label, if it exists
			label = None
			try:
				label_filenames = os.listdir(label_path)
				# If we have no label file, skip
				if len(label_filenames) == 0:
					continue

				label_path = label_path + "/" + label_filenames[-1]
				label_file = open(label_path)
				label = label_file.read().strip()[0]
			except:
				continue
			finally:
				label_file.close()

			# Augment and save/move emotion images
			num_images = max(3, int(round(len(image_filenames) / 3)))
			for filename in image_filenames[-num_images:]:

				# Skip files starting with '.'
				if filename[0] == '.':
					continue

				# Load image file
				img_path = path3 + "/" + filename
				img = Image.open(img_path)

				# Convert to grayscale
				img_gray = img.convert('1')

				# Generate location to save files
				img_dest_filepath = ROOT + "/" + IMAGE_OUT + "/" + filename

				# Save files
				img.save(img_dest_filepath)

				# Write to labels file
				f.write(filename + " " + label + "\n")

			# Augment and save/move neutral images
			for filename in image_filenames[:2]:

				# Skip files starting with '.'
				if filename[0] == '.':
					continue

				# Load image file
				img_path = path3 + "/" + filename
				img = Image.open(img_path)

				# Convert to grayscale
				img_gray = img.convert('1')

				# Generate location to save files
				img_dest_filepath = ROOT + "/" + IMAGE_OUT + "/" + filename

				# Save files
				img.save(img_dest_filepath)

				# Write to labels file
				f.write(filename + " 0" + "\n")

		print "Processed " + str(i+1) + " of " + str(len(dirs))

	f.close()


reformat_data()