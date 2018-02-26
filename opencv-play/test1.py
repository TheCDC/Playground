# https://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam
import cv2
import matplotlib.pyplot as plt
cam = cv2.VideoCapture(1)
while True:
    plt.show()
    s, im = cam.read()  # captures image
    # cv2.imshow("Test Picture", im)  # displays captured image
    plt.imshow(im)
    cv2.imwrite("test.png", im)  # writes image test.bmp to disk