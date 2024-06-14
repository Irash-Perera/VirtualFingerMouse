import numpy as np
import cv2
import pyautogui as pag

def move_mouse(x1, y1, cam_width, cam_height, screen_width, screen_height, frameR, smoothening, plocationX, plocationY, img):
    # Convert the coordinates to the screen resolution
    x3 = np.interp(x1, (frameR, cam_width - frameR), (0, screen_width))
    y3 = np.interp(y1, (frameR, cam_height - frameR), (0, screen_height))

    # Smoothen the values
    clocationX = plocationX + (x3 - plocationX) / smoothening
    clocationY = plocationY + (y3 - plocationY) / smoothening
    
    # Move the mouse
    pag.moveTo(clocationX, clocationY)
    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    
    plocationX, plocationY = clocationX, clocationY
    
    return plocationX, plocationY, img

def click_mouse(detector, img, click_status):
    # Find the distance between the two fingers
    length, img, info = detector.findDistance(8, 12, img) 
    
    if length < 40:
        if not click_status:
            cv2.circle(img, (info[4], info[5]), 15, (0, 255, 0), cv2.FILLED)
            pag.click(button='left')
            click_status = True
    else:
        if not click_status:
            cv2.circle(img, (info[4], info[5]), 15, (0, 0, 255), cv2.FILLED)
            pag.click(button='right')
            click_status = True
    return img, click_status

def scroll_up():
    pag.scroll(50)

def scroll_down():
    pag.scroll(-50)
    

    
