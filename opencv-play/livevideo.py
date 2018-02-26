# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901
import cv2
cv2.namedWindow("preview")
cv2.namedWindow("test")
vc = cv2.VideoCapture(1)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("preview", frame)
    cv2.imshow("test", gray)
    rval, frame = vc.read()
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
cv2.destroyAllWindows()
vc.release()
