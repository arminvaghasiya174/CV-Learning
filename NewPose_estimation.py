import cv2 as cv
import mediapipe as mp
import time
import pose_estimationmodules as pem
pTime=0
cTime=0
cap=cv.VideoCapture(0)
detector=pem.poseDetector()
while True:
    _,img=cap.read()
    img=detector.findpose(img)
    lmList=detector.findPosition(img)
    if len(lmList)!=0:
        print(lmList[0])
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)    
    cv.imshow('a',img)
    cv.waitKey(1)