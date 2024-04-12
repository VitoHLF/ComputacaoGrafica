import numpy as np
import cv2, time, mediapipe as mp

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            
            for id,lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                
                if id==4:
                    for id2, lm2 in enumerate(handLms.landmark):
                        cx2, cy2 = int(lm2.x*w), int(lm2.y*h)
                        if id2 == 8:
                            dist = np.sqrt((cx-cx2)**2 + (cy-cy2)**2)
                            if dist < 40:
                                """ midPx = cx2 + (dist * np.cos(cy/dist))
                                midPy = cy2 + (dist * np.sin(cx/dist)) """
                                cv2.circle(img, (cx2,cy2), 15, (255,0,255), -1)

                            #cv2.line(img, (cx,cy), (cx2,cy2), (255,0,255), 3) 

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow('Image',img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()