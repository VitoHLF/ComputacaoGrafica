import numpy as np
import cv2, time, mediapipe as mp



class Objeto(object):
    x = 0
    y = 0
    r = 20
    isLatched = False
    id = ""

    def __init__(self, x, y, r, id):
        self.x = x
        self.y = y
        self.r = r
        self.id = id
    
def makeObjeto(x,y,r,id):
    objeto = Objeto(x,y,r,id)
    return objeto

ObjetosArr = []
ObjetosArr.append(makeObjeto(200,200,20,"1"))
ObjetosArr.append(makeObjeto(400,400,25,"1"))

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

sushi1img = cv2.imread('Projeto 1\Assets\sushi01.png', cv2.IMREAD_UNCHANGED) 
hSushi,wSushi, _ = sushi1img.shape 

if not cap.isOpened():
    print("Cannot open camera")
    exit()

width = cap.get(3)
height = cap.get(4)
#print(width, height)

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, c = img.shape
    midPx, midPy = None, None #POSSIVELMENTE BUGARA VOLTE AQUI
    handLatched = False

    

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            cx1 = int(handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x*w)
            cy1 = int(handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y*h)
            cx2 = int(handLms.landmark[mpHands.HandLandmark.THUMB_TIP].x*w)
            cy2 = int(handLms.landmark[mpHands.HandLandmark.THUMB_TIP].y*h)
            cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,0),5,-1)

            dist = np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)

            if dist < 40:
                handLatched = True
                midPx = int(cx1 + (cx2-cx1)/2)
                midPy = int(cy1 + (cy2-cy1)/2)
                cv2.circle(img,(midPx,midPy),10,(255,255,255),-1)
        
    for objeto in ObjetosArr:
        if handLatched: #condição de clique
            distC = np.sqrt((midPx-objeto.x)**2 + (midPy-objeto.y)**2)
            if distC < 80 or objeto.isLatched:
                objeto.isLatched = True
                objeto.x = midPx
                objeto.y = midPy
                break
        else: objeto.isLatched = False    

    for objeto in ObjetosArr:
        #cv2.circle(img,(objeto.x,objeto.y),objeto.r, (0,0,255), -1)
        posSushiX = objeto.x
        posSushiY = objeto.y

        for y in range(hSushi):
            for x in range(wSushi):                
                if sushi1img[y,x][3] != 0 and x<width and y<height:
                    img[int(posSushiY + y - hSushi/2), int(posSushiX + x - wSushi/2)] = sushi1img[y,x][:3]

    cv2.imshow('Image',img)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
#cv2.waitKey(0)
cv2.destroyAllWindows()