"""
This is a script that periodically takes a screenshot/captures a frame from a live video camera feed of the 
Northeastern student center. 
It automatically crops out the timestamp information included on the bottom of the video camera feed.

The dependencies for this program are in `scraper_requirements.txt`, and this program can be run as
`python videoscraper.py DELAY **DURATION`
where DELAY is the minutes (int) to wait taking each frame and DURATION should the timedelta kwags (ie days=10)
to run the program for
"""

CAMERA_URL = 'http://129.10.161.241/mjpg/video.mjpg'

import cv2
from datetime import datetime, timedelta
from time import sleep
from random import random
import sys
import logging
import os

LOG_FILE = "./scraper.log"
if os.path.isfile(LOG_FILE):
    os.remove(LOG_FILE)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

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
    logging.info(f"CONFIG: Will run for {delta}")
    logging.info(f"CONFIG: Will take a photo about every {delayMin} minutes")
    logging.info(f"CONFIG: Last capture will be taken at {desiredEnd}")
    logging.info("NOW RUNNING")
    while datetime.now() < desiredEnd:
        try:
            frame = captureFrame()
        except Exception as e:
            # maybe because of wifi down for camera or for us (or for some other reason)
            # getting the frame from the camera may fail
            logging.error(f"error while getting frame. skipping this capture attempt. err={e}")
            continue
        filename = saveFrame(frame)
        logging.info(f"took a screenshot at {datetime.now()}, saved to {filename}")
        # sleep with a random delay
        nextDelay = delayMin * 60 + random() * 60 
        sleep(nextDelay)

if __name__ == "__main__":
    try:
        kwargs = dict([(key, int(val)) for (key, val) in [arg.split('=') for arg in sys.argv[2:]]])
        getManyFrames(int(sys.argv[1]), kwargs)
    except Exception as e: 
        logging.critical(e)
        raise e