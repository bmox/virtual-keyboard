import cv2
from Hand_Detection import hand_data
import math
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
colorR=(255,0,255)

cx,cy,w,h=100,100,200,200

class DragRect():
    def __init__(self,posCenter, Size=[200,200]):
        self.posCenter = posCenter
        self.size = Size
    def update(self,cursor):
        cx,cy=self.posCenter
        w,h=self.size
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
                self.posCenter=cursor
rectList=[]
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))

def findDistance(p1, p2, img,lmList_all, draw=True):
        x1, y1 = lmList_all[0][p1][1],lmList_all[0][p1][2]
        x2, y2 = lmList_all[0][p2][1],lmList_all[0][p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return  img,length     

def fancyDraw( img, bbox, l=30, t=5, rt= 1):
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]
        x1, y1 = x + w, y + h

        # cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), (0, 255, 0), t)
        cv2.line(img, (x, y), (x, y+l), (0, 255, 0), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (0, 255, 0), t)
        cv2.line(img, (x1, y), (x1, y+l), (0, 255, 0), t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + l, y1), (0, 255, 0), t)
        cv2.line(img, (x, y1), (x, y1 - l), (0, 255, 0), t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (0, 255, 0), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (0, 255, 0), t)
        return img      


while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img,lmList_all,bbox=hand_data(img,bdraw=True)
    if len(lmList_all) != 0:
        if lmList_all[0]!="NULL":
            img,l=findDistance(8, 4, img,lmList_all, draw=False)
            print(l)
            if l<30:
                cursor=lmList_all[0][8]
                for rect in rectList:
                    rect.update(cursor[1:])
    ##solid
    # for rect in rectList:
    #     cx, cy=rect.posCenter
    #     w,h=rect.size     
    #     cv2.rectangle(img,(cx-w//2, cy-h//2),(cx+w//2, cy+h//2),colorR,cv2.FILLED)
    #     bbox=[cx-w//2, cy-h//2,w,h]
    #     fancyDraw( img, bbox, l=20, t=5, rt= 1)
    ##tras
    imgNew=np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy=rect.posCenter
        w,h=rect.size     
        cv2.rectangle(imgNew,(cx-w//2, cy-h//2),(cx+w//2, cy+h//2),colorR,cv2.FILLED)
        bbox=[cx-w//2, cy-h//2,w,h]
        fancyDraw( imgNew, bbox, l=20, t=5, rt= 1)
    out=img.copy()
    alpha=0.5
    mask=imgNew.astype(bool)
    # print(mask.shape)
    out[mask]=cv2.addWeighted(img,alpha,imgNew,1-alpha,0)[mask]
    cv2.imshow("VIDEO",out)
    cv2.waitKey(1)
