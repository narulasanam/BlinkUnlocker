import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2.cv as cv


CAMERA_INDEX = 0
FACE_CLASSIFIER_PATH = "../classifiers/haarcascade_frontalface_default.xml"
EYE_CLASSIFIER_PATH = "../classifiers/haarcascade_eye.xml"
SCALE_FACTOR = 5
def imshow(img, title = ''):
    plt.axis('off')
    plt.imshow(img)
    plt.title(title)
    plt.show()

def detect_faces(image):
    faces = []
    detected = cascade.detectMultiScale(image, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
    if detected != []:
        for (x, y, w, h) in detected:  # for (x,y,w,h),n in detected:
            faces.append((x, y, w, h))
            #if len(faces) != 1:
             #   print "there is someone with you"
    return faces


if __name__ == "__main__":
    # storage = cv.CreateMemStorage()
    cascade = cv2.CascadeClassifier(FACE_CLASSIFIER_PATH)
    eye_cascade = cv2.CascadeClassifier(EYE_CLASSIFIER_PATH)
    faces = []
    image = cv2.imread("../images/image1.jpg")
    faces = detect_faces(image)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), 255, 3)
        roi = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi)
        #eyes = cv2.equalizeHist(eyes)
        #cv2.imshow("roi",roi)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            eyearea = (ex +ew/8,(ey + (eh/4.5)),ew - 2*ew/8,eh/3.0)
            eyearea_right = ex + ew/16,(ey + (eh/4.5)),(ew - 2*ew/16)/2,( eh/3.0)
            eyearea_left = ex +ew/16 +(ew - 2*ew/16)/2,(ey + (eh/4.5)),(ew - 2*ew/16)/2,(eh/3.0)

            print eyearea_left," , ",eyearea_right
            #draw the area - mGray is working grayscale mat, if you want to see area in rgb preview, change mGray to mRgba
            cv2.rectangle(roi,(int(eyearea_left[0]),int(eyearea_left[1])),(int(eyearea_left[0])+int(eyearea_left[2]),int(eyearea_left[1])+int(eyearea_left[3])), (255,0,255), 2)
            cv2.rectangle(roi,(int(eyearea_right[0]),int(eyearea_right[1])),(int(eyearea_right[0])+int(eyearea_right[2]),int(eyearea_right[1])+int(eyearea_right[3])), (255,0,255), 2)

            reye = roi[ey:ey + eh, ex:ex + ew]
            eyes = eye_cascade.detectMultiScale(roi)
            # if len(eyes) > 2:
            #     print "more than two eyes"
            #     continue
            # eyes = cv2.equalizeHist(eyes)
            # cv2.imshow("roi",roi)
            #print "eyes :", eyes
            counter = 0
            for (ex, ey, ew, eh) in eyes:
                if len(eyes[counter]) is 4:
                    cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                    eye = roi[ey:ey + eh, ex:ex + ew]
                    eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
                    ret,thresh = cv2.threshold(eye,100,255,cv2.THRESH_BINARY)
                    #eye = cv2.equalizeHist(eye)
                    #eye = cv2.GaussianBlur(eye, (7, 7), 4)
                    #detect circles in the image
                    #cv2.imshow("eye is ",eye)
                    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    cv2.drawContours(eye, contours, -1, (255,255,255), -1)
                    for cnt in contours:
                        area = cv2.contourArea(cnt)    # Blob area
                        rect = cv2.boundingRect(cnt) # Bounding box
                        x,y,w,h = cv2.boundingRect(cnt)
                        radius = w/2                     # Approximate radius
                        # if area > 0:
                        #     cv2.circle(eye, (x + radius, y + radius), radius,(0,0,0), 2)
                        try:
                            print (area >= 20 and abs(1 - (w / h)) <= 0.2)
                            print "area :",area,"value 1:",abs(1 - (w / h)),"value 2:",abs(1 - (area / (cv.CV_PI * pow(radius, 2))))
                        except ZeroDivisionError:
                            pass

                        if area >= 30 and abs(1 - (w / h)) <= 0.2 and abs(1 - (area / (cv.CV_PI * pow(radius, 2)))) <= 0.5:
                            print "drawing"
                            cv2.circle(eye,(x + radius, y + radius), radius,(0,0,0), 2)
                    #print contours
                    #cv2.imshow("contour",eye)
                    circles = None
                    #circles = cv2.HoughCircles(eye, cv.CV_HOUGH_GRADIENT, 2.5, 100)
                    #circles = cv2.HoughCircles(eye, cv.CV_HOUGH_GRADIENT, 3, 100)
                    if counter is 0:
                        cv2.imshow("leftEye", eye)
                        #cv2.imwrite("../images/eye.jpg",eye)
                        #print "left"
                        counter += 1
                    else:
                        cv2.imshow("rightEye", eye)
                        #print "right"
                    #print "circles is :",circles
                    if circles is not None:
                        # convert the (x, y) coordinates and radius of the circles to integers
                        circles = np.round(circles[0, :]).astype("int")
                        # loop over the (x, y) coordinates and radius of the circles
                        for (x, y, r) in circles:
                            # draw the circle in the output image, then draw a rectangle
                            # corresponding to the center of the circle
                            cv2.circle(eye, (x, y), r, (0, 0, 255), 4)

                        # show the output image
                        cv2.imshow("pupil",eye)
                        #cv2.imshow("output", np.hstack([image, eye]))
            #cv2.imshow("roi",roi)
    imshow(image, "image")
    pressedKey = cv2.waitKey(10)
cv2.destroyAllWindows()
