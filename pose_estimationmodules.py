import cv2 as cv
import mediapipe as mp
import time
import math

class poseDetector():
    def __init__(self,mode=False,complexity=1,landmarks=True,enable_seg=False,smooth_seg=True,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.complexity=complexity
        self.landmarks=landmarks
        self.enable_seg=enable_seg
        self.smooth_seg=smooth_seg
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.complexity,self.landmarks,self.enable_seg,self.smooth_seg,self.detectionCon,self.trackCon) 
        self.mpDraw=mp.solutions.drawing_utils

    def findpose(self,img,draw=True):
        img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results=self.pose.process(img1)
        # print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self,img,draw=True):
        self.lmList=[]
        if self.results.pose_landmarks:
            self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),10,(255,0,0),cv.FILLED)
        return self.lmList

    def findAngle(self,img,p1,p2,p3,draw=True):
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        x3,y3=self.lmList[p3][1:]
        angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angle<0:
            angle+=360
        if draw:
            cv.line(img,(x1,y1),(x2,y2),(255,255,255),3)
            cv.line(img,(x2,y2),(x3,y3),(255,255,255),3)
            cv.circle(img,(x1,y1),10,(0,0,255),cv.FILLED)
            cv.circle(img,(x1,y1),15,(0,0,255),2)
            cv.circle(img,(x2,y2),10,(0,0,255),cv.FILLED)
            cv.circle(img,(x2,y2),15,(0,0,255),2)
            cv.circle(img,(x3,y3),10,(0,0,255),cv.FILLED)
            cv.circle(img,(x3,y3),15,(0,0,255),2)
            cv.putText(img,str(int(angle)),(x2-50,y2+50),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        return angle

def main():
    pTime=0
    cTime=0
    cap=cv.VideoCapture(0)
    detector=poseDetector()
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

if __name__=="__main__":
    main()