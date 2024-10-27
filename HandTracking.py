import cv2 as cv
import mediapipe as mp
import time

cap=cv.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands() 
mpDraw=mp.solutions.drawing_utils
pTime=0
cTime=0
while True:
    _,img=cap.read() 
    img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=hands.process(img1)
    # print(results)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # for id,lm in enumerate(handLms.landmark):
            #     h,w,c=img.shape
            #     cx,cy=int(lm.x*w),int(lm.y*h)
            #     print(id,cx,cy)
            #     if id==0:
            #         cv.circle(img,(cx,cy),10,(255,0,0),cv.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)    
    cv.imshow('a',img)
    cv.waitKey(1)