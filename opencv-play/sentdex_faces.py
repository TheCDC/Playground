"""https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/"""
import numpy as np
import cv2
import os
import sys
import enum
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--video-file', type=str, default=None, help='Choose a video file.')
parser.add_argument(
    '-c', '--camera', type=int, default=-1, help='Choose index of webcam.')
parser.add_argument(
    '-m',
    '--mode',
    type=str,
    default='swap',
    help=
    'Choose algorithm from "swap" and "insert". Insert requires webcam and video file.'
)
args = parser.parse_args()


class FaceFinder:
    def __init__(self):
        # multiple cascades:
        # https://github.com/Itseez/opencv/tree/master/data/haarcascades
        parent_dir = os.path.abspath(os.path.dirname(__file__))
        # https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        self.face_cascade = cv2.CascadeClassifier(
            os.path.join(parent_dir, 'cascades',
                         'haarcascade_frontalface_default.xml'))
        # https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
        self.eye_cascade = cv2.CascadeClassifier(
            os.path.join(parent_dir, 'cascades', 'haarcascade_eye.xml'))

    def find_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = list(self.face_cascade.detectMultiScale(gray, 1.3, 3))
        face_images = []
        for (x, y, w, h) in faces:
            face_images.append(image[y:y + h, x:x + w].copy())
        return face_images


facefinder = FaceFinder()
capture_type = None
if args.video_file:
    webcam_stream = cv2.VideoCapture(args.video_file)
    # print(f'Video FPS: {cap.get(cv2.CV_CAP_PROP_FPS)}')
else:
    webcam_stream = cv2.VideoCapture(args.camera)

# webcam_stream = cv2.VideoCapture(0)
all_faces_img = None
frame_index = 0
while 1:

    ret, webcam_img = webcam_stream.read()
    face_images = facefinder.find_faces(webcam_img)
    if len(face_images) > 1:
        all_faces_img = np.concatenate(
            tuple(cv2.resize(im, (100, 100)) for im in face_images), axis=1)
    elif len(face_images) > 0:
        all_faces_img = cv2.resize(face_images[0], (100, 100))
    # swap faces around
    if len(face_images) > 1:
        for index, face in enumerate(face_images):
            ii = (index + 1) % len(face_images)
            x, y, w, h = faces[ii]
            webcam_img[y:y + h, x:x + w] = cv2.resize(face, (w, h))

    cv2.imshow('webcam_img', webcam_img)
    if all_faces_img is not None:
        cv2.imshow('all faces', all_faces_img)
    k = cv2.waitKey(30) & 0xff
    print(k)
    if k == 27:
        break
    elif k == 83:
        frame_index += 100
        webcam_stream.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    elif k == 81:
        frame_index -= 100
        webcam_stream.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    frame_index += 1

webcam_stream.release()
cv2.destroyAllWindows()
