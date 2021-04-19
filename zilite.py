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
import RPi.GPIO as GPIO
plt.ion()

GPIO.setmode(GPIO.BCM)
stream = io.BytesIO()
camera = PiCamera()
camera.resolution = (320, 256)
camera.framerate = 60
camera.start_recording(stream, format='h264', bitrate=20000000)
raw_capture = PiRGBArray(camera, size=(320, 256))
time.sleep (0.1)
GPIO.setup(14,GPIO.OUT)
GPIO.output(14,GPIO.HIGH)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    cv.imshow("video", image)
    
    #parveido attelu melnbaltu
    #slieksnis labam apgaismojumam (man led gaisma - galda lampa)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    retval, thresholded = cv.threshold(gray, 60, 255, 0)
    cv.imshow("slieksnis", thresholded)
    
    #pielabo formu, degradejot vai pieaudzejot elementu
    closed = cv.erode(cv.dilate(thresholded, kernel, iterations=1), kernel, iterations=1)
    cv.imshow("precizeta forma", closed)
    
    #atrod un uzzime visas konturas
    contours, hierarchy = cv.findContours(closed, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    drawing = np.copy(image)
    cv.drawContours(drawing, contours, -1, (255, 0, 0), 2)
    
    #kontura ipasibas
    for contour in contours:
        area = cv.contourArea(contour)
        bounding_box = cv.boundingRect(contour)
        extend = area / (bounding_box[2] * bounding_box [3])
        if extend > 0.8:
            continue
        if area < 500:
            continue

        #apkart konturam uzzime elipsi
        try:
            ellipse = cv.fitEllipse(contour)
            cv.ellipse(drawing, box=ellipse, color=(0, 0, 255))
            (x, y), (MA, ma), angle = cv.fitEllipse(contour)
            L = np.pi / 4 * MA * ma
            (x,y),radius = cv.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            K = np.pi*radius*radius
            cv.circle(drawing,center,radius,color=(0, 255, 0))
            m = cv.moments(contour)
            if m['m00'] != 0:
                center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
                cv.circle(drawing, center, 3, (0, 255, 0), -1)
        except:
            pass
        #paradit konturu
        cv.imshow("Drawing", drawing)
        header = ["area", "L", "K", "radius", "radius*2", "int(x)", "int(y)", "datetime.datetime.now()"]
        arr = [area, L, K, radius, radius*2, int(x), int(y), datetime.datetime.now()]
        print(arr)
        with open('dati.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(arr)
        
       
         
     #video uznemsanu izsledz ar q
    key = cv.waitKey(1) & 0xFF
    raw_capture.truncate(0)
    if key == ord("q"):
        break

   
   
        
