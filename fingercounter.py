from turtle import left
import cv2 as cv
import Handtrackingmodules as htm

wCam,hCam=640,480
cap=cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=htm.handDetector(detectionCon=0.75)
finger_coor=[(8,6),(12,10),(16,14),(20,18)]
thumb_coor=(4,3)
def counter(lmList):
    Count=0
    p=[]
    #right hand
    if lmList[thumb_coor[0]][1]>lmList[thumb_coor[1]][1]:
        Count+=1
        p.append(1)
    else:p.append(0)
    for coor in finger_coor:
        if lmList[coor[0]][2]<lmList[coor[1]][2]:
            Count+=1
            p.append(1)
        else :
            p.append(0)
            
    
    #left hand
    # if lmList[thumb_coor[0]][1]<lmList[thumb_coor[1]][1]:
    #     Count+=1
    return Count,p
while True:
    _,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        count,finger_list=counter(lmList)
        print(count,finger_list)
        if finger_list[0]==1 and finger_list[1]==0 and finger_list[2]==0 and finger_list[3]==0 and finger_list[4]==0:
            cv.putText(img,"A",(20,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        elif count==5:
            cv.putText(img,"B",(20,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        # elif count==5:

            

    else:
        cv.putText(img,"Hand is not detected!",(20,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.imshow('a',img)
    cv.waitKey(1)