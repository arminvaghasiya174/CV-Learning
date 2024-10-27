# 1.Import Image
# 2. Find Hand Landmarks
# 3.Check which fingers are up
# 4.If selection mode-Two finger are up
# 5.If drawing mode-Index finger is up
import cv2 as cv
import numpy as np
import Handtrackingmodules as htm

cap=cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=htm.handDetector(detectionCon=0.85)
drawcolor=(255,0,255)
brushthickness=15
eraserthickness=100
xp,yp=0,0
imgcanvas=np.zeros((720,1280,3),np.uint8)
while True:
    _,img=cap.read()
    img=cv.flip(img,1)
    img=detector.findHands(img,False)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        xp,yp=0,0
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        fingers=detector.FingerUp()
        Count=fingers.count(1)
        if Count==1:
            drawcolor=(255,0,255)
        elif Count==2:
            drawcolor=(255,0,0)
        elif Count==3:
            drawcolor=(0,255,0)
        elif Count==4:
            drawcolor=(0,0,0)
        cv.circle(img,(x1,y1),15,drawcolor,cv.FILLED)
        if xp==0 and yp==0:
            xp,yp=x1,y1
        if drawcolor==(0,0,0):
            cv.line(img,(xp,yp),(x1,y1),drawcolor,eraserthickness)
            cv.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,eraserthickness)
        else:
            cv.line(img,(xp,yp),(x1,y1),drawcolor,brushthickness)
            cv.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,brushthickness)
        xp,yp=x1,y1
    img1=cv.cvtColor(imgcanvas,cv.COLOR_BGR2GRAY)
    _,img2=cv.threshold(img1,50,255,cv.THRESH_BINARY_INV)
    img2=cv.cvtColor(img2,cv.COLOR_GRAY2BGR)
    img=cv.bitwise_and(img,img2)
    img=cv.bitwise_or(img,imgcanvas)
    img=cv.addWeighted(img,0.5,imgcanvas,0.5,0)
    cv.imshow('a',img)
    # cv.imshow('a',imgcanvas)
    cv.waitKey(1)