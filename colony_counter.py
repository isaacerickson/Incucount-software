import cv2
import numpy as np;
import os
import datetime
from tkinter import *
from PIL import Image, ImageTk

WIDTH = 450
HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GAMEFILE = os.path.dirname(__file__)
thresh = 100
camera_num = 0
img_file = "test12.png"
text_file = "data.pdf"
gray_can_width = 225
gray_can_height = 180
can_width = 225
can_height = 180
number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
image_type = "Positive"

root = Tk()
root.title ("INCUCOUNT")
root.configure(background='white')
root.geometry(f"{WIDTH}x{HEIGHT}")
w = Label(root, text ='', bg="white", font = "100")
t = Label(root, text ='', bg="white", font = "80")
a = Label(root, text ='Insert Petri Plate and press the button', bg="white", font = "80")
w.pack()
t.pack()
a.pack()
can = Canvas(root, height=can_height, width=can_width)
can.place(x=WIDTH-can_width, y=HEIGHT-can_height)
img = Image.open(img_file)
img = img.resize((can_width, can_height))
img = ImageTk.PhotoImage(img)
gray_can = Canvas(root, height=gray_can_height, width=gray_can_width)
gray_can.place(x=0, y=HEIGHT-gray_can_height)
gray_image = cv2.imread(img_file)
gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
thresh, gray_image = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)
gray_image = Image.fromarray(gray_image)
gray_image = gray_image.resize((can_width, can_height))
gray_image = ImageTk.PhotoImage(gray_image)

def replace_images():
    global img
    global can
    global gray_image
    global gray_can
    global thresh
    img = Image.open(img_file)
    img = img.resize((can_width, can_height))
    img = ImageTk.PhotoImage(img)
    gray_image = cv2.imread(img_file)
    gray_image = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    (thresh, gray_image) = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)
    gray_image = Image.fromarray(gray_image)
    gray_image = gray_image.resize((can_width, can_height))
    gray_image = ImageTk.PhotoImage(gray_image)
    can.create_image((can_width//2, can_height//2), image=img)
    gray_can.create_image((gray_can_width//2, gray_can_height//2), image=gray_image)

def count_colonies(bwi):
    global th, threshed, cnts, s1, s2, xcnts, colony_count, dot_count
    th, threshed = cv2.threshold(bwi, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    s1 = 3
    s2 = 20
    xcnts = []
    for cnt in cnts:
        if s1<cv2.contourArea(cnt) <s2:
            xcnts.append(cnt)
    try:
        dot_count.destroy()
    except NameError:
        pass
    colony_count = len(xcnts)
    dot_count = Label(root, text="Colony Count {}".format((colony_count)))
    dot_count.place(x=0, y=60)

def store_data():
    updated_time = datetime.datetime.now()
    second = updated_time.second
    minute = updated_time.minute
    hour = updated_time.hour
    day = updated_time.day
    month = updated_time.month
    year = updated_time.year
    minute = str(minute)
    if minute in number_list:
        minute = "0" + minute
    if second in number_list:
        second = "0" + second
    with open(os.path.join(GAMEFILE, text_file), 'a') as f:
        f.write(f"Colony Count: {colony_count}, Time: {month}/{day}/{year}, {hour}:{minute}:{second}\n")
    f.close()

def readSample():
    global thresh, cap, image_type
    image_type = image_type_clicked.get()
    cap = cv2.VideoCapture(camera_num)
    s, im = cap.read()
    cv2.imwrite(img_file, im)
    imagedata_original = cv2.imread(img_file, 1)
    detectorobj = cv2.SimpleBlobDetector_create()
    keypoint_info = detectorobj.detect(imagedata_original)
    originalImage = cv2.imread(img_file)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    thresh, bwi = cv2.threshold(grayImage, thresh, 255, cv2.THRESH_BINARY)
    count_colonies(bwi)
    cap.release()
    bwi = np.zeros((1, 1))
    blank_img = np.zeros((10, 100))
    blobs = cv2.drawKeypoints(imagedata_original, keypoint_info, np.array([]), WHITE, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    replace_images()
    store_data()

def change_thresh():
    global thresh
    global thresh_text
    thresh_text.destroy()
    text = entry1.get()
    try:
        thresh = int(text)
    except ValueError:
        thresh = 0
    thresh_text = Label(root, text="Thresh: {}".format(thresh))
    thresh_text.place(x=0, y=0)

def change_camera():
    global camera_num
    global camera_text
    camera_text.destroy()
    text = entry2.get()
    try:
        camera_num = int(text)
    except ValueError:
        camera_num = 0
        print("HELLOW")
    camera_text = Label(root, text="Camera number: {}".format(camera_num))
    camera_text.place(x=0, y=20)

title = Label(root, text="Plate Reader", bg="white")
title.pack()
thresh_text = Label(root, text="Thresh: {}".format(thresh))
thresh_text.place(x=0, y=0)
thresh_button = Button(root, text="Threshold", command=change_thresh)
thresh_button.pack()
entry1 = Entry(root, width=20)
entry1.pack()
camera_text = Label(root, text="Camera number: {}".format(camera_num))
camera_text.place(x=0, y=20)
camera_button = Button(root, text="Camera number", command=change_camera)
camera_button.pack()
entry2 = Entry(root, width=20)
entry2.pack()
image_type_text = Label(root, text=f"Image type: {image_type}")
image_type_text.place(x=0, y=40)
image_type_clicked = StringVar()
image_type_clicked.set(f"Image type: {image_type}")
image_type_drop = OptionMenu(root, image_type_clicked, "Positive", "Negative")
image_type_drop.pack()
button = Button(root, text="Read Sample", command=readSample)
button.pack()
can.create_image((can_width//2, can_height//2), image=img)
gray_can.create_image((gray_can_width//2, gray_can_height//2), image=gray_image)
root.mainloop()
cv2.destroyAllWindows()
