import cv2
import time
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

detector = htm.handDetector()
tipIds = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img=detector.findHands(img)

    lmlist = detector.findposition(img, draw=False)
    #print(lmlist)

    if len(lmlist)!=0:
        fingers = []

        #thumb
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #four fingers
        for id in range(1,5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)

        totalfingers = fingers.count(1)
        print(totalfingers)

        cv2.rectangle(img, (20,225), (170,425), (0,255,0),cv2.FILLED)
        cv2.putText(img, str(totalfingers), (45,375),cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    #if lmlist[8][2] < lmlist[6][2]:
            #print('index finger open')
    cv2.imshow("Image",img)
    cv2.waitKey(1)