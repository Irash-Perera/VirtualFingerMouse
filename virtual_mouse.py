import cv2
import numpy as np
import hand_tracker as ht
import time
import pyautogui as pag

cam_width, cam_height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

while True:
    ret, img = cap.read()
    
    cv2.imshow('Image', img)
    cv2.waitKey(1)