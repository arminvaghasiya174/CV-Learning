import cv2 as cv
import mediapipe as mp
import time

cap=cv.VideoCapture(0)
cTime=0
pTime=0
mpDraw=mp.solutions.drawing_utils
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec=mpDraw.DrawingSpec(thickness=2,circle_radius=1)
while True:
    _,img=cap.read()
    img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=faceMesh.process(img1)
    # print(results)
    if results.multi_face_landmarks:
        for facelms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img,facelms,mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec) #mpFaceMesh.FACEMESH_TESSELATION
            for id,lm in enumerate(facelms.landmark):
                ih,iw,ic=img.shape
                x,y=int(lm.x*iw),int(lm.y*ih)
                print(id,x,y)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,f'FPS:{int(fps)}',(20,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv.imshow('a',img)
    cv.waitKey(1)