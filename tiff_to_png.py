import os
from PIL import Image

in_path = '../data/jaffeimages/tiff/'
out_path = '../data/jaffeimages/png/'

filenames = os.listdir(in_path)
for fn in filenames:
	im = Image.open(in_path + fn)
	new_fn = fn[:-5] + '.png'
	im.save(out_path + new_fn, 'png')