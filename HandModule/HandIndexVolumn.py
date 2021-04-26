import cv2
import time
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
''' 
#Andre Miras
thanks to him to support the lb
'''
##########################
hCam = 480
wCam = 640
#########################

caption = cv2.VideoCapture(0)
caption.set(3,wCam)
caption.set(4,hCam)
cTime = 0
pTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
voRange = volume.GetVolumeRange()
#print(volume.GetVolumeRange())
minvolu = voRange[1]
maxvolu = voRange[0]

detector = htm.handDetector(detectionCon=0.6)
while True:
    success,img = caption.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1,y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy = ( x1 + x2 ) // 2, ( y1 + y2 ) // 2

        cv2.circle(img, (cx,cy), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,100,255),3)

        length = math.hypot(x2 - x1,y2 - y1)
        #print(length)
        # xai tay 50<x<300
        # do to dai tu -65<x<-0
        vol = np.interp(length,[50,150],[maxvolu,minvolu])
        volume.SetMasterVolumeLevel(vol, None)



        if length < 60:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

cTime = time.time()
fps = 1/(cTime - pTime)
pTime = cTime
cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)

cv2.imshow("Hands",img)
cv2.waitKey(1)
