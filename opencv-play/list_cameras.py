import cv2


def list_cameras():
    found = list()
    for i in range(10):
        opened = cv2.VideoCapture(i).isOpened()
        if opened:
            found.append(i)
    return found
