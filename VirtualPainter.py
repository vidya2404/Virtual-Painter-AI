import cv2
import numpy as np
import time
import os
import imutils
import HandTrackingModule as htm


folderPath = "Header"
mylist = os.listdir(folderPath)
#print(mylist)

overlayList = []
for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))
header = overlayList[0]

drawColor = (0,0,0)
brushThickness = 15
eraserThickness = 50

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionconfidence=0.8)
xp,yp = 0,0
imgCanvas = np.zeros((480, 640, 3), np.uint8)

while True:

    # 1
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2
    img = detector.findHands(img)
    lmlist = detector.findposition(img, draw=False)

    if len(lmlist)!=0:
        xp, yp = 0, 0
        #print(lmlist)

        #tip of index and middle fingers
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        # 3
        fingers = detector.FingersUp()
        #print(fingers)

        # 4
        if fingers[1] and fingers[2]:
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
            print("Selection mode")
            if y1 < 90:
                if 30<x1<130:
                    header = overlayList[2]
                    drawColor = (255,0,255)
                elif 180<x1<300:
                    header = overlayList[1]
                    drawColor = (255,0,0)
                elif 330<x1<430:
                    header = overlayList[3]
                    drawColor = (0,255,0)
                elif 460<x1<600:
                    header = overlayList[0]
                    drawColor = (0,0,0)
        # 5
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            print("Drawing mode")
            if xp==0 and yp ==0:
                xp, yp = x1,y1

            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)


            cv2.line(img, (xp,yp), (x1,y1),drawColor,brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

   # seetting the header image
    img[0:90, 0:640] = header
    img = imutils.resize(img, width=2000)
    img = imutils.resize(img, height=820)


    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break












# 1. Import image
# 2. Find Hand Landmarks
# 3. check which fingers are up
# 4. If selection mode - Two fingers are up
# 5. If Drawing mode - Index finger is up
