# https://stackoverflow.com/questions/2601194/displaying-a-webcam-feed-using-opencv-and-python#11449901

import cv2
import random
cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

FRAME_WIDTH = frame.shape[0]
FRAME_HEIGHT = frame.shape[1]
# initialize all the image clips
clips = list()
for i in range(12):
    width = random.randint(0, FRAME_WIDTH - 1)
    height = random.randint(0, FRAME_HEIGHT - 1)
    x = random.randint(0, FRAME_WIDTH - 1 - width)
    y = random.randint(0, FRAME_HEIGHT - 1 - height)
    clip = frame[x:x + width, y:y + height]
    clips.append(clip)
i = 0
cursor = 0
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    if i % 2 == 0:
        # get a new clip
        width = random.randint(0, FRAME_WIDTH - 1)
        height = random.randint(0, FRAME_HEIGHT - 1)
        x = random.randint(0, FRAME_WIDTH - 1 - width)
        y = random.randint(0, FRAME_HEIGHT - 1 - height)
        clip = frame[x:x + width, y:y + height].copy()
        # replace an old clip
        clips[cursor % len(clips)] = clip
        cursor += 1
    for clip in clips:
        width = clip.shape[0]
        height = clip.shape[1]
        newx = random.randint(0, FRAME_WIDTH - 1 - width)
        newy = random.randint(0, FRAME_HEIGHT - 1 - height)
        frame[newx:newx + width, newy:newy + height] = clip
    key = cv2.waitKey(1)
    if key > -1:
        print('key', key, end=' ')
        print(chr(key))
        if key == 32:
            cv2.imwrite('live_shot.png', frame)
    if key == 27:  # exit on ESC
        break
    i += 1
cv2.destroyWindow("preview")
cv2.destroyAllWindows()
vc.release()
