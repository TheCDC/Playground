import cv2
import numpy as np


class ColorPicker:
    def __init__(self, window_name):
        self.x = None
        self.y = None
        self.window_name = window_name
        self.clicked = False
        self.color = np.array((0, 0, 0))
        self.hsv = None
        self.frame = None
        cv2.setMouseCallback(window_name, self.handle_event)

    def handle_event(self, event, x, y, flags, param):
        # print(event)
        self.x = x
        self.y = y
        self.clicked = True
        self.color = self.frame[y, x]
        print('clicked color', self.color)

    def transform(self, frame):
        self.frame = frame.copy()
        # self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print(self.color)
        mask = cv2.inRange(self.frame, self.color - 30, self.color + 30)
        res = cv2.bitwise_and(self.frame, self.frame, mask=mask)

        # frame[:, :, :] = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
        frame[:, :, :] = res


# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901
cv2.namedWindow("preview")
vc = cv2.VideoCapture(-1)

rval, frame = vc.read()
drawer = ColorPicker('preview')
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    drawer.transform(frame)
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
