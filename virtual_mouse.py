import cv2
import numpy as np
import hand_tracker as ht
import time
import pyautogui as pag


cam_width, cam_height = 640, 480
frameR = 100
smoothening = 3

pTime = 0
plocationX, plocationY = 0, 0
clocationX, clocationY = 0, 0

detector = ht.handDetector(maxHands=1)
screen_width, screen_height = pag.size()

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

while True:
    ret, img = cap.read()
    
    img = detector.findHands(img) # Draw the hand landmarks
    lmList, bbox = detector.findPosition(img) # Get the hand landmarks coordinates and bounding box
    
    if len(lmList) !=0:
        x1, y1 = lmList[8][1:] # Index finger tip
        x2, y2 = lmList[12][1:] # Middle finger tip
        
        # Check which fingers are up
        fingers = detector.fingersUp()
        
        cv2.rectangle(img, (frameR, frameR), (cam_width - frameR, cam_height - frameR), (255, 0, 255), 2)
        
        # IF the index finger is up, move the mouse
        if fingers[1]==1 and fingers[2]==0 and fingers[0] == 0:
            #Convert the coordinates to the screen resolution
            x3 = np.interp(x1, (frameR, cam_width - frameR), (0, screen_width))
            y3 = np.interp(y1, (frameR, cam_height - frameR), (0, screen_height))

            # Smoothen the values
            clocationX = plocationX + (x3 - plocationX) / smoothening
            clocationY = plocationY + (y3 - plocationY) / smoothening
            
            #Move the mouse
            pag.moveTo(screen_width - clocationX, clocationY) # Invert the x-axis
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            
            plocationX, plocationY = clocationX, clocationY
        
        # IF the index and middle fingers are up, click the mouse
        if fingers[1]==1 and fingers[2]==1 and fingers[0] == 0:
            # Find the distance between the two fingers
            length, img, info = detector.findDistance(8, 12, img) 
            
            if length < 40:
                cv2.circle(img, (info[4], info[5]), 15, (0, 255, 0), cv2.FILLED)
                pag.click()

        
    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    
    # Display the image
    cv2.imshow('Image', img)
    cv2.waitKey(1)