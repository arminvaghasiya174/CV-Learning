import cv2 as cv
import mediapipe as mp
import time

cap=cv.VideoCapture(0)
cTime=0
pTime=0
mpFace=mp.solutions.face_detection
mpDraw=mp.solutions.drawing_utils
Face=mpFace.FaceDetection(0.75)
while True:
    _,img=cap.read()
    img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=Face.process(img1)
    if results.detections:
        for id,detection in enumerate(results.detections):
            # print(id,detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box)
            # mpDraw.draw_detection(img,detection)
            bboxc=detection.location_data.relative_bounding_box
            ih,iw,ic=img.shape
            bbox=int(bboxc.xmin*iw), int(bboxc.ymin*ih),\
                int(bboxc.width*iw), int(bboxc.height*ih)
            cv.rectangle(img,bbox,(255,0,255),2)
            cv.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,f'FPS:{int(fps)}',(20,70),cv.FONT_HERSHEY_PLAIN,3,(0,255,0),2)
    cv.imshow('a',img)
    cv.waitKey(1)