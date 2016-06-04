# client3.py on local machine
#!/usr/bin/env python

#!/usr/bin/env python

import socket
import time
import cv2
import sys
import numpy as np

#TCP_IP = 'localhost'
TCP_IP = '52.53.196.158'
TCP_PORT = 5000
# filename = 'results.png'
filename = 'results.txt'
BUFFER_SIZE = 65507

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

clock_start = time.clock()

with open(filename, 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print data
        if not data:
            f.close()
            print 'file close() break'
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
print('connection closed')

clock_end = time.clock()
duration_clock = clock_end - clock_start
print 'clock:  start = ',clock_start, ' end = ',clock_end
print 'clock:  duration_clock = ', duration_clock


frame_counter = 0
with open(filename, 'r') as f:
    while True:
        frame_counter +=1
        data = f.readline()
        # print "data", data
        img_name = "test_img_" + str(frame_counter) + ".jpg"
        img = cv2.imread(img_name)
        cv2.imshow(data,img)
        cv2.waitKey(0)
        if not data:
            f.close()
            print 'file close() break'
            break








