__author__ = 's5narula'
# standard setup
import numpy as np
import matplotlib.pyplot as plt
import cv2

# setup capture
camera = cv2.VideoCapture(0)

# reduce frame size to speed it up
w = 640
#camera.set(cv2.CV_CAP_PROP_FRAME_WIDTH, w)
#camera.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, w * 3/4)

# capture loop
while True:

    # get frame
    ret, frame = camera.read()
    frame = cv2.flip(frame,1)
    cv2.imshow('frame',frame)

    if cv2.waitKey(5) == 32:
        cv2.imwrite("image1.jpg",frame)
        cv2.imshow("hello",frame)
        print "taken"

    if cv2.waitKey(5) == 27:
        break

# clean up
cv2.destroyAllWindows()
camera.release()
