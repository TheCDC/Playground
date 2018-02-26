import numpy as np
import cv2
# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901
cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    # BGR colors
    cv2.line(frame, (0, 0), (100, 100), (0, 255, 0), 5)
    font = cv2.FONT_HERSHEY_SIMPLEX
    message = 'lol!'
    pos = (0, 200)
    color = (255, 255, 255)
    letter_thickness = 2
    size = 1
    cv2.putText(frame, message, pos, font, size, color, letter_thickness,
                cv2.LINE_AA)
    key = cv2.waitKey(1)
    print('key', key, end=' ')
    if key > -1:
        print(chr(key))
        if key == 32:
            cv2.imwrite('live_shot.png', frame)
    else:
        print()
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
