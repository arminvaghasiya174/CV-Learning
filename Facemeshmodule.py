import cv2 as cv
import mediapipe as mp
import time

class FaceMesh:
    def __init__(self,staticmode=False,maxFaces=2,refinelms=False,minDetCon=0.5,minTrackCon=0.5):
        self.staticmode=staticmode
        self.maxFaces=maxFaces
        self.refinelms=refinelms
        self.minDetCon=minDetCon
        self.minTrackCon=minTrackCon
        self.mpDraw=mp.solutions.drawing_utils
        self.mpFaceMesh=mp.solutions.face_mesh
        self.faceMesh=self.mpFaceMesh.FaceMesh(self.staticmode,self.maxFaces,self.refinelms,self.minDetCon,self.minTrackCon)
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=2,circle_radius=1)

    def FindFace(self,img,draw=True):
        img1=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results=self.faceMesh.process(img1)
        faces=[]
        if self.results.multi_face_landmarks:
            for facelms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,facelms,self.mpFaceMesh.FACEMESH_CONTOURS,self.drawSpec,self.drawSpec) #mpFaceMesh.FACEMESH_TESSELATION
                    face=[]
                for id,lm in enumerate(facelms.landmark):
                    ih,iw,ic=img.shape
                    x,y=int(lm.x*iw),int(lm.y*ih)
                    face.append([id,x,y])
                    # if draw:
                        # cv.putText(img,str(id),(x,y),cv.FONT_HERSHEY_PLAIN,0.5,(255,0,0),1)
            faces.append(face)
        return img,faces

    # def FindPosition(self,img,faceno=0,draw=True):
    #     lmList=[]
    #     if self.results.multi_face_landmarks:
    #         myFace=self.results.multi_face_landmarks[faceno]
    #         for id,lm in enumerate(myFace.landmark):
    #             ih,iw,ic=img.shape
    #             x,y=int(lm.x*iw),int(lm.y*ih)
    #             lmList.append([id,x,y])
    #             if draw:
    #                 cv.circle(img,(x,y),10,(255,0,0),cv.FILLED)
    #     return lmList

def main():
    cap=cv.VideoCapture(0)
    cTime=0
    pTime=0
    detector=FaceMesh()
    while True:
        _,img=cap.read()
        img,faces=detector.FindFace(img)
        # lmList=detector.FindPosition(img,0,False)
        # print(lmList)
        if len(faces)!=0:
            print(len(faces))
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv.putText(img,f'FPS:{int(fps)}',(20,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv.imshow('a',img)
        cv.waitKey(1)

if __name__=="__main__":
    main()