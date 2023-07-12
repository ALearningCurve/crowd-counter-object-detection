# the target:
# http://129.10.161.241/mjpg/video.mjpg

CAMERA_URL = 'http://129.10.161.241/mjpg/video.mjpg'

import cv2
from datetime import datetime, timedelta
from time import sleep
from random import random
import sys

def captureFrame(): 
    cap = cv2.VideoCapture(CAMERA_URL)
    while True:
        gotFrame, frame = cap.read()
        if gotFrame: 
            cap.release()
            # the bottom 20ish pixels is a time stamp banner
            return frame[:-20]

def saveFrame(frame):
    filename = datetime.today().strftime('frames/%Y_%m_%d__%H_%M.jpg')
    cv2.imwrite(filename, frame)
    return filename


def getManyFrames(delayMin, durationParameters):
    delta = timedelta(**durationParameters)
    desiredEnd = datetime.now() + delta
    print("INFO:")
    print(f"\tWill run for {delta}")
    print(f"\tWill take a photo about every {delayMin} minutes")
    print(f"\tLast capture will be taken at {desiredEnd}\n")
    print("RUN TIME:")

    while datetime.now() < desiredEnd:
        frame = captureFrame()
        filename = saveFrame(frame)
        print(f"[ ] took a screenshot at {datetime.now()}, saved to {filename}")
        # sleep for about 10 minutes
        sleep(delayMin * 60 + random() * 60)

if __name__ == "__main__":
    kwargs = dict([(key, int(val)) for (key, val) in [arg.split('=') for arg in sys.argv[2:]]])
    getManyFrames(int(sys.argv[1]), kwargs)