# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901
import cv2
import numpy as np
cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    edges = cv2.Canny(frame, 150, 200)
    max_corners = 100
    quality = 0.01
    neighbor_distance = 10
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    corners = np.int0(corners)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(frame, (x, y), 3, 255, -1)
    frame = cv2.add(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), frame)
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(1)
    if key > -1:
        print('key', key, chr(key))
        if key == 32:
            cv2.imwrite('live_shot.png', frame)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
cv2.destroyAllWindows()
vc.release()
