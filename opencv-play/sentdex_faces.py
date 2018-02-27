"""https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/"""
import numpy as np
import cv2
import os

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier(
    os.path.join('cascades', 'haarcascade_frontalface_default.xml'))
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier(
    os.path.join('cascades', 'haarcascade_eye.xml'))

cap = cv2.VideoCapture(1)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = list(face_cascade.detectMultiScale(gray, 1.3, 5))
    face_images = []
    for index, (x, y, w, h) in enumerate(faces):
        face_images.append(img[y:y + h, x:x + w].copy())
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0),
                          2)
    if len(face_images) > 1:
        for index, face in enumerate(face_images):
            cv2.imshow(f'face {index}', face)
            ii = (index + 1) % len(face_images)
            x, y, w, h = faces[ii]
            img[y:y + h, x:x + w] = cv2.resize(face, (w, h))

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()