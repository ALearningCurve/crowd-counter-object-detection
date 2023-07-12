# the target:
# http://129.10.161.241/mjpg/video.mjpg

CAMERA_URL = 'http://129.10.161.241/mjpg/video.mjpg'

import cv2
import numpy as np
from datetime import datetime
import imutils

def captureFrame(): 
    cap = cv2.VideoCapture(CAMERA_URL)
    while True:
        gotFrame, frame = cap.read()
        if gotFrame: 
            cap.release()
            return frame
    return frame

def saveFrame():
    frame = captureFrame()
    # the bottom 20ish pixels is a time stamp banner
    frame = frame[:-20] 
    filename = datetime.today().strftime('frames/%Y_%m_%d__%H_%M.jpg')
    cv2.imwrite(filename, frame)

def readFrame():
    frame = cv2.imread('frames/2023_07_11__18_40.jpg')
    cv2.imshow("FRAME ", frame)
  
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    # closing all open windows
    cv2.destroyAllWindows()

def drawBoxes(): 
    # Initializing the HOG person
    # detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
   
    # Reading the Image
    image = cv2.imread('frames/2023_07_11__18_40.jpg')
    
    # Resizing the Image
    image = imutils.resize(image,
                        width=min(400, image.shape[1]))
    
    # Detecting all the regions in the 
    # Image that has a pedestrians inside it
    (regions, _) = hog.detectMultiScale(image, 
                                        winStride=(4, 4),
                                        padding=(4, 4),
                                        scale=1.05)
    
    # Drawing the regions in the Image
    for (x, y, w, h) in regions:
        cv2.rectangle(image, (x, y), 
                    (x + w, y + h), 
                    (0, 0, 255), 2)
    
    # Showing the output Image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
   
cv2.destroyAllWindows()
drawBoxes()