import cv2
import mediapipe as mp
import time

caption = cv2.VideoCapture(0)

mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils
#insert pre time and current time

    # frame ko thay doi
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    #print(result.multi_hand_landmarks)
    # Ve cac point cua tay
    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            #tracking các index(1,20)
            for id, lm in enumerate(handlm.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                if id == 0:
                    cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img,handlm,mpHand.HAND_CONNECTIONS)
    #tính Fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_ITALIC,2,(200,15,200),3)
    cv2.imshow("Hand",img)
    cv2.waitKey(1)

