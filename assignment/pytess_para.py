import pytesseract
import cv2, imutils
import numpy as np
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('test4.png')
org = img.copy()
fin = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

H, W = img.shape[0], img.shape[1]

from collections import defaultdict

dic = defaultdict(list)

boxes = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(boxes['text'])

for i in range(1, n_boxes):
    key, x, y, w, h = boxes['par_num'][i], boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
    dic[key].append([x, y, w, h])

print(img.shape)  # h,w,dims
for d in dic:
    print(d)
    for all_points in dic[d]:
        x, y, w, h = all_points
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
        #cv2.putText(img, str(d), (x,y),cv2.FONT_HERSHEY_COMPLEX,2, (0,0,255),2)

# filter 2 : now getting real boxes
kernel = np.ones((3, 3))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
for _ in range(3):
    blur = cv2.GaussianBlur(blur, (7, 7), 0)
    dilate = cv2.dilate(blur, kernel, iterations=5)
    erode = cv2.erode(dilate, kernel, iterations=5)

filter = cv2.GaussianBlur(erode, (7, 7), 0)
_, thresh = cv2.threshold(filter, 127, 255, 0)

# drawing boxes
cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(fin, (x, y), (x + w, y + h), (0, 0, 255), 3)

img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_AREA)
org = cv2.resize(org, (640, 480), interpolation=cv2.INTER_AREA)
gray = cv2.resize(gray, (640, 480))
fin = cv2.resize(fin, (640, 480))
cv2.imshow('mat', img)
cv2.imshow('mat', fin)
cv2.imshow('gray', gray)
cv2.imshow('org', org)
cv2.waitKey(0)
