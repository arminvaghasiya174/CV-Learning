import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import math
import Handtrackingmodules as htm
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume 

wcam,hcam=640,480
cap=cv.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
vol,volper,volbar=0,0,400
detector=htm.handDetector(detectionCon=0.75)
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
VolRange=volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0,None)
minVol=VolRange[0]
maxVol=VolRange[1]
while True:
    _,img=cap.read()
    img=detector.findHands(img,draw=False)
    lmList=detector.findPosition(img,draw=False)
    # print(lmList)
    if len(lmList)!=0:
        # print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv.circle(img,(x1,y1),10,(255,0,255),cv.FILLED)
        cv.circle(img,(x2,y2),10,(255,0,255),cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(255,0,0),4)
        cv.circle(img,(cx,cy),10,(255,0,255),cv.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        # print(length)
        #Hand Range 50-100
        #Volume Range -65 -0
        vol=np.interp(length,[50,300],[minVol,maxVol])
        volbar=np.interp(length,[50,300],[400,150])
        volper=np.interp(length,[50,300],[0,100])
        volume.SetMasterVolumeLevel(vol,None)
        if length < 50:
            cv.circle(img,(cx,cy),10,(0,255,0),cv.FILLED)
    cv.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv.rectangle(img,(50,int(volbar)),(85,400),(255,0,0),cv.FILLED)  
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,f'FPS:{int(fps)}',(40,50),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv.putText(img,f'{int(volper)}%',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv.imshow("a",img)
    cv.waitKey(1)