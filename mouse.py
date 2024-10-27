import cv2 as cv
import numpy as np
import Handtrackingmodules as htm
import autopy

wCam,hCam=640,480
frameR=100
smoothing=7
plocx,plocy=0,0
clocx,clocy=0,0
cap=cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(maxHands=1)
wScr,hScr=autopy.screen.size()
while True:
    _,img=cap.read()
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        fingers=detector.FingerUp()
        cv.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            clocx=plocx + (x3-plocx)/smoothing
            clocy=plocy + (y3-plocy)/smoothing
            autopy.mouse.move(wScr-clocx,clocy)
            cv.circle(img,(x1,y1),15,(255,0,255),cv.FILLED)
            plocx,plocy=clocx,clocy
        if fingers[1]==1 and fingers[2]==1:
            length,img,infoline=detector.findDistance(8,12,img)
            if length<40:
                cv.circle(img,(infoline[4],infoline[5]),15,(0,255,0),cv.FILLED) 
                autopy.mouse.click()  
    cv.imshow('a',img)
    cv.waitKey(1)

