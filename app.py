import cv2
from Hand_Detection import hand_data
import math
from time import sleep
import numpy as np
from pynput.keyboard import Controller
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
final_text=""
keyboard=Controller()
Keys=[["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L",";"],
    ["Z","X","C","V","B","N","M",",",".","/"]]

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


def drawAll(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        position_is=[button.pos[0],button.pos[1],button.size[0],button.size[1]]
        fancyDraw(img=img,bbox=position_is,l=20, t=5, rt= 0)
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img









class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text
  


buttonList=[]       
for i in range(len(Keys)):
    for j,key in enumerate(Keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key))
        

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
      

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img,lmList_all,bbox=hand_data(img,bdraw=True)
    img=drawAll(img,buttonList)
    if len(lmList_all) != 0:
        if lmList_all[0]!="NULL":
            # print(lmList_all)
            for button in buttonList:
                x,y=button.pos
                w,h=button.size
                # print(lmList_all[0][8][1])
                if x< lmList_all[0][8][1]<x+w and y<lmList_all[0][8][2]<y+h:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    img,l=findDistance(8, 4, img,lmList_all, draw=False)
                    # print(l)
                    if l<20:
                        keyboard.press(button.text)
                        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                        final_text+=button.text
                        sleep(0.15)
    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,final_text,(60,430),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)


    
    cv2.imshow("VIDEO",img)
    cv2.waitKey(1)