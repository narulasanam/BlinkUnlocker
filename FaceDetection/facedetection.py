import cv2

CAMERA_INDEX = 0


def detect_faces(image):
    faces = []
    detected = cascade.detectMultiScale(image, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
    if detected != []:
        print 'face detected'
        print detected
        for (x, y, w, h) in detected:  # for (x,y,w,h),n in detected:
            faces.append((x, y, w, h))
    return faces


if __name__ == "__main__":
    # print 'creating window' #
    cv2.namedWindow("Video")

    capture = cv2.VideoCapture(CAMERA_INDEX)
    # storage = cv.CreateMemStorage()

    cascade = cv2.CascadeClassifier('../classifiers/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('../classifiers/haarcascade_eye.xml')
    faces = []
    i = 0
    c = -1
    while (c == -1):
        retval, image = capture.read()
        # print 'acq img frm' #

        # Only run the Detection algorithm every 5 frames to improve performance
        if i % 5 == 0:
            faces = detect_faces(image)
            print 'came back'
            print faces
        for (x, y, w, h) in faces:
            print 'drawing rectangle'
            cv2.rectangle(image, (x, y), (x + w, y + h), 255, 3)
            roi = image[y:y + h, x:x + w]
            print 'roi'
            eyes = eye_cascade.detectMultiScale(roi)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                print 'showing img'
        cv2.imshow("Video", image)
        i += 1
        c = cv2.waitKey(10)
        if (c == 27):
            # escape
            break;
