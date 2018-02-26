import numpy as np
import cv2


class CircleDrawer:

    def __init__(self, window_name):
        self.x = None
        self.y = None
        self.window_name = window_name
        self.clicked = False

        cv2.setMouseCallback(window_name, self.handle_event)

    def handle_event(self, event, x, y, flags, param):
        # print(event)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y
            self.clicked = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.clicked = False
        if self.clicked:
            cv2.circle(frame, (x, y), 100, (255, 255, 255), 5)

# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

rval, frame = vc.read()
drawer = CircleDrawer('preview')
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    # BGR colors
    key = cv2.waitKey(1)
    if key > -1:
        print('key', key, end=' ')
        print(chr(key))
        if key == 32:
            cv2.imwrite('live_shot.png', frame)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
