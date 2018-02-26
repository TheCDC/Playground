# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
import cv2
import numpy as np
# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901
cv2.namedWindow("preview")
vc = cv2.VideoCapture(-1)
VID_WIDTH = 640
VID_HEIGHT = 480
vc.set(3, VID_WIDTH)
vc.set(4, VID_HEIGHT)
kernel_size = 5
blur_kerner = np.ones((5, 5), np.float32) / kernel_size**2

# define a video file output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (VID_WIDTH, VID_HEIGHT))
# out = cv2.VideoWriter('output.avi', -1, 20.0, (VID_HEIGHT, VID_HEIGHT))

rval, frame = vc.read()
while rval:
    rval, frame = vc.read()

    threshholded = cv2.adaptiveThreshold(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    # blurred = cv2.filter2D(threshholded, -1, blur_kerner)
    blurred = cv2.medianBlur(threshholded, kernel_size)
    edges = cv2.Canny(frame, 100, 150)
    # convert grayscale (one color channel) to BRG by duplicating
    # color channels
    edges_brg = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    # equivalent line:
    # edges_brg = cv2.merge((edges, edges, edges))
    # edges_brg = cv2.merge((edges, edges, edges))
    edges_brg[:, :, (0, 2)] = 0

    overlayed = cv2.add(frame, edges_brg)
    # write expects an image with shape (x,y,3)
    out.write(overlayed)
    cv2.imshow("preview", frame)
    cv2.imshow("edges", overlayed)
    cv2.imshow("threshholded", blurred)
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

out.release()
vc.release()
cv2.destroyAllWindows()
