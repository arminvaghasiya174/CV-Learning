import cv2 as cv
import mediapipe as mp
import time

mpPose=mp.solutions.pose
pose=mpPose.Pose()
mpDraw=mp.solutions.drawing_utils
cap=cv.VideoCapture(0)
pTime=0
cTime=0
while True:
    _,img=cap.read()
    img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=pose.process(img1)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c=img.shape
            cx,cy=int(lm.x*w),int(lm.y*h)
            print(id,cx,cy)
            if id==0:
                cv.circle(img,(cx,cy),10,(255,0,0),cv.FILLED)
    cv.imshow("a",img)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,str(int(fps)),(70,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.waitKey(1)