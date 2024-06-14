import cv2
import hand_tracker as ht
import time
import pyautogui as pag
import operations as ops

cam_width, cam_height = 640, 480
frameR = 100
smoothening = 2

pTime = 0
plocationX, plocationY = 0, 0
clocationX, clocationY = 0, 0

detector = ht.handDetector(maxHands=1)
screen_width, screen_height = pag.size()

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

click_status = False  # State variable to keep track of click status

while True:
    ret, img = cap.read()
    
    img = cv2.flip(img, 1)

    img = detector.findHands(img)  # Draw the hand landmarks
    lmList, bbox = detector.findPosition(img)  # Get the hand landmarks coordinates and bounding box
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        
        # Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        
        cv2.rectangle(img, (frameR, frameR), (cam_width - frameR, cam_height - frameR), (255, 0, 255), 2)
        
        # If the index finger is up, move the mouse
        if fingers[1] == 1 and fingers[2] == 0:
            plocationX, plocationY, img = ops.move_mouse(x1, y1,
                                                         cam_width, cam_height, 
                                                         screen_width, screen_height, 
                                                         frameR, 
                                                         smoothening, 
                                                         plocationX, plocationY, 
                                                         img)
            
        # If the index and middle fingers are up, click the mouse
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            img, click_status = ops.click_mouse(detector,
                                                img,
                                                click_status)
        else:
            click_status = False
        
        # If all fingers are up, scroll up
        if all(f == 1 for f in fingers):
            ops.scroll_up()
        
        # If all fingers are down, scroll down
        if all(f == 0 for f in fingers):
            ops.scroll_down()
            
        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            # Terminal the program
            cv2.putText(img, "Exiting...", (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.imshow('Image', img)
            cv2.waitKey(2000)
            break

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    # Display the image
    cv2.imshow('Image', img)
    cv2.waitKey(1)
