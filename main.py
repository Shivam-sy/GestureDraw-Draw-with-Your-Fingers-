import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np


cap = cv2.VideoCapture(0) 
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def getHandInfo(img):
      hands, img = detector.findHands(img, draw=True, flipType=True)

      if hands:
        
        hand1 = hands[0]  
        lmList = hand1["lmList"]  

        fingers1 = detector.fingersUp(hand1)
        print(fingers1)
        return fingers1,lmList
      
      else:
          return None,None
    

def draw(info,prev_pos,canvas):
    fingers1,lmList=info
    current_pos=None

    if fingers1 ==[0,1,0,0,0]:
        current_pos=lmList[8][0:2]
        if prev_pos is None:
            prev_pos=current_pos
        cv2.line(canvas,current_pos,prev_pos,color=(235, 206, 135),thickness=5)
    return current_pos ,canvas


prev_pos =None
canvas =None
image_combined =None


while True:
    success, img = cap.read()
    img=cv2.flip(img,flipCode=1)

    if canvas is None:
        canvas=np.zeros_like(img)



    info=getHandInfo(img)
    if info:
        fingers1, lmList=info
        print(fingers1)
        prev_pos,canvas=draw(info,prev_pos,canvas)

    image_combined = cv2.addWeighted(img, 0.80, canvas, 0.20, 0)


    if not success:
        print("Failed to capture image")
        break


        print(" ")  
   # cv2.imshow("Image", img)
   # cv2.imshow("Canvas", canvas)
    cv2.imshow("Image Combined",image_combined)


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
