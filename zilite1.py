import io
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
import time
import numpy as np
import cv2 as cv
import random
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import os



stream = io.BytesIO()
camera = PiCamera()
camera.resolution = (320, 256)
camera.framerate = 60
camera.start_recording(stream, format='h264', bitrate=20000000)
raw_capture = PiRGBArray(camera, size=(320, 256))
time.sleep (0.1)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    retval, thresholded = cv.threshold(gray, 70, 255, 0)
    closed = cv.erode(cv.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
    thresholded, contours, hierarchy = cv.findContours(closed, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
     
    for contour in contours:
        area = cv.contourArea(contour)
        bounding_box = cv.boundingRect(contour)
        extend = area / (bounding_box[2] * bounding_box [3])
        if extend > 0.8:
            continue
        if area < 100:
            continue
        try:
            (x,y),radius = cv.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            cv.circle(image,center,radius,color=(255, 0, 0))            
#             ellipse = cv.fitEllipse(contour)
#             cv.ellipse(image, box=ellipse, color=(0, 255, 0))         
        except:
            pass
        arr = [area, datetime.datetime.now()]
        print(arr)
        with open('dati.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(arr)               
            
    cv.imshow("video", image)
    key = cv.waitKey(1) & 0xFF
    raw_capture.truncate(0)
    if key == ord("q"):
        break
  
cv.destroyAllWindows()

   
   
        
