import io
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2 as cv
import random
from itertools import count
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

stream = io.BytesIO()
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 60
camera.start_recording(stream, format='h264', bitrate=20000000)
raw_capture = PiRGBArray(camera, size=(160, 128))
time.sleep (0.1)
GPIO.setup(14,GPIO.OUT)
GPIO.output(14,GPIO.HIGH)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)


plt.ion()

#lai varetu veikt  formas parveidosanu (to dara ar binaro attelu), no attela iegust strukturejoso elementu
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    cv.imshow("video", image)
    
    #parveido attelu melnbaltu
    #slieksnis labam apgaismojumam (man led gaisma - galda lampa)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    retval, thresholded = cv.threshold(gray, 50, 255, 0)
    cv.imshow("slieksnis", thresholded)
    
    #pielabo formu, degradejot vai pieaudzejot elementu
    closed = cv.erode(cv.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
    cv.imshow("precizeta forma", closed)
    
    #atrod un uzzime visas konturas
    thresholded, contours, hierarchy = cv.findContours(closed, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    drawing = np.copy(image)
    cv.drawContours(drawing, contours, -1, (255, 0, 0), 2)
    
    #kontura ipasibas
    for contour in contours:
        area = cv.contourArea(contour)
        bounding_box = cv.boundingRect(contour)
        extend = area / (bounding_box[2] * bounding_box [3])
        if extend > 0.8:
            continue
        if area < 100:
            continue
        #apkart konturam uzzime elipsi
        try:
            ellipse = cv.fitEllipse(contour)
            cv.ellipse(drawing, box=ellipse, color=(0, 255, 0))
        except:
            pass
        #paradit konturu
        cv.imshow("Drawing", drawing)
        print(area, time.timezone)

        plt.plot([1.4, 2.5])
        axes = plt.gca()
        axes.plot([3.1, 2.2])
       
          
     #video uznemsanu izsledz ar q
    key = cv.waitKey(1) & 0xFF
    raw_capture.truncate(0)
    if key == ord("q"):
        break

   
   
        
