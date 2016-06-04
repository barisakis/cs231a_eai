import cv2
import sys
from PIL import Image
import numpy as np
import socket
import pickle
import struct ### new code

faceCascade = cv2.CascadeClassifier('/Users/barisakis/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)
IMG_SIZE = (250, 250)

UDP_IP = socket.gethostbyaddr("52.53.196.158")[0]
UDP_PORT = 60001

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

clientsocket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

# number of frames sent to server
max_frame = 10
clientsocket.sendto(str(max_frame), (UDP_IP, UDP_PORT))
# counter for images sent to network
frame_counter = 0
# f = open('new_test_data.txt','a')
while frame_counter < max_frame:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    # print frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    # If no faces found, skip image
    if len(faces) == 0:
        continue

    # Find largest face
    faces.tolist().sort( lambda f1, f2: int(f1[2] * f1[3]) - int(f2[2] * f2[3]) )
    face = [faces[0]]

    # Draw a rectangle around the faces
    for (x, y, w, h) in face:
        frame_counter += 1
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        img = gray[y:(y+h), x:(x+h)]
        # cv2.imshow("Cropped found" ,img)
        # cv2.waitKey(500)
        # resize
        img = cv2.resize(img, IMG_SIZE)
        # img_name = "test_img_7" + str(frame_counter) + ".jpg"
        img_name = "test_img_" + str(frame_counter) + ".jpg"
        print img_name
        cv2.imwrite(img_name, img)
        # f.write(img_name)
        # Send cropped face to server
        img = img.flatten()
        data = img.tostring()
        # print len(data), img
        clientsocket.sendto(data, (UDP_IP, UDP_PORT))

    # Display the resulting frame
    cv2.imshow('Video Input', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
