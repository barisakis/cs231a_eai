import socket
import sys
import time
import caffe
# import cv2
# import pickle
from PIL import Image
import numpy as np
# import struct ## new

DEPLOY_PATH = '../cnn/deploy.prototxt'
MODEL_PATH = '../snapshots/lenet_iter_2000.caffemodel'
MEAN_IMAGE_PATH = '../data/mean_image.binaryproto'

emotion_dict = {0:'neutral',
		1:'anger',
		2:'disgust',
		3:'fear',
		4:'happy',
		5:'sad',
		6:'surprise'}

def loadCNN():
	caffe.set_device(0)
	caffe.set_mode_gpu()

	blob = caffe.proto.caffe_pb2.BlobProto()
	data = open(MEAN_IMAGE_PATH, 'rb').read()
	blob.ParseFromString(data)
	mean_img = np.array(caffe.io.blobproto_to_array(blob))[0]

	net = caffe.Classifier(DEPLOY_PATH,
        	               MODEL_PATH,
                	       mean=mean_img,
                      	       raw_scale=255,
                	       image_dims=(250, 250))
	return net

def runCNN(net, img, clock_start):
	clock_end = time.clock()
	pred = net.predict([img])[0]
	return pred
	
net = loadCNN()


UDP_IP = socket.gethostbyaddr("52.53.196.158")[0]
UDP_PORT = 60001

s = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
s.bind((UDP_IP, UDP_PORT))

print "UDP Host IP:", UDP_IP
print "UDP Host port:", UDP_PORT

filename='cnn_results.txt'
f = open(filename,'a')
print "opened", filename
frame_counter = -1
max_frame = float('Inf')
while True:
	# print max_frame, frame_counter
	if frame_counter == -1:
		max_frame, addr = s.recvfrom(65507) # buffer size is 65507 bytes
		f = open(filename,'wb')
		# print max_frame
	elif int(max_frame) == int(frame_counter):
		print "CLOSE"
		f.close()
		frame_counter = -2
		# s.close()
		# break
	else:
		clock_start = time.clock()
		data, addr = s.recvfrom(65507) # buffer size is 65507 bytes
		frame = np.fromstring(data, dtype=np.uint8)
		#print frame.shape
		#frame1 = np.reshape(frame, (250,250))
		frame2 = np.reshape(frame, (250,250,1)) / 255.0
		# print frame
		#scores1 = runCNN(net, img, clock_start)
		scores2 = net.predict([frame2])[0]
		#print img
		# print frame2
		#label = scores.argmax()
		print scores2
		scores2 = find_neutral_dif(scores2)
		emotipred =  emotion_dict[scores2.argmax()]
		print "MAX: ", emotipred
		f.write("MAX: " + str(emotipred) + " \n")
		# scores2 = sorted(scores2)
		for i, score in enumerate(scores2):
			emoti_label =  emotion_dict[i]
			print "Label: ", emoti_label, "  Score:   ", score
			f.write("Label: "+ str(emoti_label)+ "  Score:   "+ str(score)+"\n")
		# f.write(emotipred+'\n')
	frame_counter += 1

