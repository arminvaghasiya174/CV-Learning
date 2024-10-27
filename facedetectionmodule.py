import cv2 as cv
import mediapipe as mp
import time

class FaceDetection:
    def __init__(self,mindetectCon=0.5):
        self.mindetectCon=mindetectCon
        self.mpFace=mp.solutions.face_detection  
        self.mpDraw=mp.solutions.drawing_utils
        self.Face=self.mpFace.FaceDetection(self.mindetectCon)
    
    def findface(self,img,draw=True):
        img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results=self.Face.process(img1)
        bboxs=[]
        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
            # print(id,detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box)
            # mpDraw.draw_detection(img,detection)
                bboxc=detection.location_data.relative_bounding_box
                ih,iw,ic=img.shape
                bbox=int(bboxc.xmin*iw), int(bboxc.ymin*ih),\
                    int(bboxc.width*iw), int(bboxc.height*ih)
                bboxs.append([id,bbox,detection.score])
                if draw:
                    img=self.fancyDraw(img,bbox)
                    # cv.rectangle(img,bbox,(255,0,255),2)
                    cv.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        return img,bboxs

    def fancyDraw(self,img,bbox,l=30,t=6):
        x,y,w,h=bbox
        x1,y1=x+w,y+h
        cv.rectangle(img,bbox,(255,0,255),1)
        cv.line(img,(x,y),(x+l,y),(255,0,255),t)
        cv.line(img,(x,y),(x,y+l),(255,0,255),t)
        cv.line(img,(x1,y),(x1-l,y),(255,0,255),t)
        cv.line(img,(x1,y),(x1,y+l),(255,0,255),t)
        cv.line(img,(x,y1),(x+l,y1),(255,0,255),t)
        cv.line(img,(x,y1),(x,y1-l),(255,0,255),t)
        cv.line(img,(x1,y1),(x1-l,y1),(255,0,255),t)
        cv.line(img,(x1,y1),(x1,y1-l),(255,0,255),t)
        return img

def main():
    cap=cv.VideoCapture(0)
    cTime=0
    pTime=0
    detector=FaceDetection()
    while True:
        _,img=cap.read()
        img,box=detector.findface(img)
        # print(box)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(img,f'FPS:{int(fps)}',(20,70),cv.FONT_HERSHEY_PLAIN,3,(0,255,0),2)
        cv.imshow('a',img)
        cv.waitKey(1)

if __name__=="__main__":
    main()