import cv2 as cv
import numpy as np
import pose_estimationmodules as pem

cap=cv.VideoCapture(0)
detector=pem.poseDetector()
Count=0
dir=0
while True:
    _,img=cap.read()
    img=detector.findpose(img,False)
    lmList=detector.findPosition(img,False)
    img=cv.resize(img,(1280,720))
    if len(lmList)!=0:
        #right
        # angle=detector.findAngle(img,12,14,16)
        #left
        angle=detector.findAngle(img,11,13,15)
        per=np.interp(angle,(210,310),(0,100))
        if per==100:
            if dir==0:
                Count+=0.5
                dir=1
        if per==0:
            if dir==1:
                Count+=0.5
                dir=0
        cv.putText(img,str(Count),(50,100),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)        
    cv.imshow('a',img)
    cv.waitKey(1)