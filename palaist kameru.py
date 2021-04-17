import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

GPIO.setup(14,GPIO.OUT)

GPIO.output(14,GPIO.HIGH)
GPIO.setup(18,GPIO.OUT)

GPIO.output(18,GPIO.HIGH)

while True:
    success, img = cap.read()
    cv2.imshow("video",img)
   
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    