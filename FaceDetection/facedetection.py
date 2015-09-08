# -*- coding: utf-8 -*-
from IPython import Application
import cv2
import cv2.cv as cv
from Tkinter import *
import tkMessageBox as tm
from FaceDetection import helper

CAMERA_INDEX = 0
FACE_CLASSIFIER_PATH = "../classifiers/haarcascade_frontalface_default.xml"
# EYE_CLASSIFIER_PATH = "../classifiers/haarcascade_eye.xml"
EYE_CLASSIFIER_PATH = "../classifiers/haarcascade_eye_tree_eyeglasses.xml"
# EYE_CLASSIFIER_PATH = "../classifiers/haarcascade_lefteye_2splits"
SCALE_FACTOR = 5
track_count = 0
passw = ""

def detect_faces(image, cascade):
    faces = []
    detected = cascade.detectMultiScale(image, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
    if detected != []:
        for (x, y, w, h) in detected:  # for (x,y,w,h),n in detected:
            faces.append((x, y, w, h))
            if len(faces) != 1:
               tm.showerror("Security error", "There is some one with you")
               print "there is someone with you"
    return faces


def track_eyes(mode, left_num=0, right_num=0, both_num =0):
    print "mode:",mode

    global track_count
    if track_count is 0:
        passw = entry_2.get()
        track_count = 1

    left_close_counter = 0
    right_close_counter = 0
    both_close_counter = 0

    cv2.namedWindow("Video")
    capture = cv2.VideoCapture(CAMERA_INDEX)
    # storage = cv.CreateMemStorage()
    cascade = cv2.CascadeClassifier(FACE_CLASSIFIER_PATH)
    eye_cascade_left = cv2.CascadeClassifier(EYE_CLASSIFIER_PATH)
    eye_cascade_right = cv2.CascadeClassifier(EYE_CLASSIFIER_PATH)
    faces = []
    frame_counter = 0
    while True:
        retval, image = capture.read()
        image = cv2.flip(image, 1)
        if frame_counter % SCALE_FACTOR == 0:
            faces = detect_faces(image, cascade)
        for (x, y, w, h) in faces:
            faceCenter = (((x + w) / 2.0), ((y + h) / 2.0))
            faceDiameter = h - y
            cv2.rectangle(image, (x, y), (x + w, y + h), 255, 3)
            eyearea = (x + w / 8, (y + (h / 4.5)), w - 2 * w / 8, h / 3.0)
            eyearea_right = x + w / 16, (y + (h / 4.5)), (w - 2 * w / 16) / 2, (h / 3.0)
            eyearea_left = x + w / 16 + (w - 2 * w / 16) / 2, (y + (h / 4.5)), (w - 2 * w / 16) / 2, (
                h / 3.0)

            cv2.rectangle(image, (int(eyearea_left[0]), int(eyearea_left[1])),
                          (int(eyearea_left[0]) + int(eyearea_left[2]), int(eyearea_left[1]) + int(eyearea_left[3])),
                          (0, 0, 255), 2)
            cv2.rectangle(image, (int(eyearea_right[0]), int(eyearea_right[1])), (
                int(eyearea_right[0]) + int(eyearea_right[2]), int(eyearea_right[1]) + int(eyearea_right[3])),
                          (0, 0, 255), 2)
            if mode != 0:
                # roi = image[y:y + h, x:x + w]
                roi_image_right = image[eyearea_left[1]:eyearea_left[1] + eyearea_left[3],
                                  eyearea_left[0]:eyearea_left[0] + eyearea_left[2]]
                roi_image_left = image[eyearea_right[1]:eyearea_right[1] + eyearea_right[3],
                                 eyearea_right[0]:eyearea_right[0] + eyearea_right[2]]
                # cv2.imr("face",roi)
                # print eyearea_left, " , ", eyearea_right, " , ", faceCenter
                roi_image_left_gray = cv2.cvtColor(roi_image_left, cv2.COLOR_BGR2GRAY)
                roi_image_right_gray = cv2.cvtColor(roi_image_right, cv2.COLOR_BGR2GRAY)
                #cv2.imshow("roi_image",roi_image_left)
                eye_left = eye_cascade_left.detectMultiScale(roi_image_left_gray)
                eye_right = eye_cascade_right.detectMultiScale(roi_image_right_gray)
                # eyes = cv2.equalizeHist(eyes)

                # print "eyes :", eyes
                counter = 0
                print eye_left, ",", eye_right
                if mode is 1:
                    if eye_left is not ():
                        left_close_counter = 0
                        for (ex, ey, ew, eh) in eye_left:
                            if len(eye_left[counter]) is 4:
                                eye_left = roi_image_left[ey:ey + eh, ex:ex + ew]
                                cv2.rectangle(roi_image_left, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                                print "lefteye: ", helper.interim_code
                    else:
                        left_close_counter += 1
                        if left_close_counter is 5:
                            if left_num < 4:
                                left_num += 1
                            helper.interim_code = "L" + str(left_num)
                            #helper.interim_code = "α" + str(left_num)
                elif mode is 2:
                    if eye_right is not ():
                        right_close_counter = 0
                        for (ex, ey, ew, eh) in eye_right:
                            if len(eye_right[counter]) is 4:
                                print "inside eye_right"
                                eye_right = roi_image_left[ey:ey + eh, ex:ex + ew]
                                cv2.rectangle(roi_image_right, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                    else:
                        print "in else"
                        right_close_counter += 1
                        if right_close_counter is 5:
                            if right_num < 4:
                                right_num += 1
                            # for right gamma γβα
                            helper.interim_code = 'R' + str(right_num)
                            #helper.interim_code = 'β' + str(right_num)
                else:
                    #mode is 3
                    if eye_left is not () and eye_right is not ():
                        both_close_counter = 0
                        for (ex, ey, ew, eh) in eye_left:
                            if len(eye_left[counter]) is 4:
                                eye_left = roi_image_left[ey:ey + eh, ex:ex + ew]
                                cv2.rectangle(roi_image_left, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                        for (ex, ey, ew, eh) in eye_right:
                            if len(eye_right[counter]) is 4:
                                eye_right = roi_image_left[ey:ey + eh, ex:ex + ew]
                                cv2.rectangle(roi_image_right, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                    else:
                        both_close_counter += 1
                        if both_close_counter is 5:
                            if both_num < 4:
                                both_num += 1
                            # for B input beta
                            helper.interim_code = "B" + str(both_num)
                            #helper.interim_code = "γ" + str(both_num)
        cv2.imshow("Video", image)
        frame_counter += 1
        pressedKey = cv2.waitKey(10)
        if pressedKey == 36:
            global paasw
            passw = passw + helper.interim_code
            entry_2.delete(0,'end')
            print entry_2.get()
            print "passw: ",passw
            entry_2.insert(0, passw)
            break
        elif pressedKey is 70 or pressedKey is 102:
            global passw
            passw = passw + helper.interim_code
            entry_2.delete(0,'end')
            print entry_2.get()
            print "passw: ",passw
            entry_2.insert(0, passw)
            helper.interim_code = ""
            cv2.destroyAllWindows()
            left_close_counter = 0
            left_num = 0
            track_eyes(1)
        elif pressedKey is 72 or pressedKey is 104:
            global passw
            passw = passw + helper.interim_code
            entry_2.delete(0,'end')
            print entry_2.get()
            print "passw: ",passw
            entry_2.insert(0, passw)
            helper.interim_code = ""
            cv2.destroyAllWindows()
            right_close_counter = 0
            right_num = 0
            track_eyes(2)
        elif pressedKey is 66 or pressedKey is 98:
            global passw
            passw = passw + helper.interim_code
            entry_2.delete(0,'end')
            print entry_2.get()
            print "passw: ",passw
            entry_2.insert(0, passw)
            helper.interim_code = ""
            cv2.destroyAllWindows()
            both_close_counter = 0
            both_num = 0
            track_eyes(3)
        elif pressedKey is 32:
            global passw
            passw = passw + helper.interim_code
            entry_2.delete(0,'end')
            print "passw: ",passw
            entry_2.insert(0, passw)
            helper.interim_code = ""
            cv2.destroyAllWindows()
            right_close_counter = 0
            both_close_counter = 0
            left_close_counter = 0
            left_num = 0
            right_num= 0
            both_num = 0
            track_eyes(0)

    cv2.destroyAllWindows()

def destroy():
    cv2.destroyAllWindows()


def key(event, eyeDetectorButton='$', code=helper.current_status):
    print("pressed", event.char)
    print code
    if event.char is eyeDetectorButton:
        if code is 0:
            helper.current_entry_value = ""
            helper.current_status = 1
            track_eyes(0)
        else:
            destroy()


def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)


def login_btn_clicked():
    username = entry_1.get()
    password = entry_2.get()

    #print password
    degree_sign = u'\N{DEGREE SIGN}'

    #γβα
    #if username == "sanam" and password == "asα1β1γ1$":
    if username == "sanam" and password == "asL1R1B1$":
        tm.showinfo("Login info", "Welcome Sanam")
    else:
        print username
        print password
        tm.showerror("Login error", "Incorrect username or password")


root = Tk()

frame = Frame(root,bg="yellow")
frame.master.minsize(300,200)
label_1 = Label(frame, text="Username",bg ="yellow")
label_2 = Label(frame, text="Password",bg = "yellow")
entry_1 = Entry(frame)
entry_2 = Entry(frame, show="*")
#entry_2 = Entry(frame)

#print("here is your checkmark: " + u'\u0391');

label_1.grid(row=0, sticky=E)
entry_1.grid(row=0, column=1)
label_2.grid(row=1, sticky=E)
entry_2.grid(row=1, column=1)

checkbox = Checkbutton(frame,bg="yellow", text="Keep me logged in")
checkbox.grid(columnspan=2)

logbtn = Button(frame, text="Login", command=login_btn_clicked)
logbtn.grid(columnspan=2)

label_1.pack(padx=0,pady=0)
entry_1.pack()
label_2.pack()
entry_2.pack()
checkbox.pack(padx=5, pady=5)
logbtn.pack(padx=10, pady=10)

entry_2.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.pack(fill='both', expand=True)
root.mainloop()
