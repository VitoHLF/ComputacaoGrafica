import numpy as np
import cv2, time, mediapipe as mp
import random
from datetime import datetime


class Sushi(object):
    x = 0
    y = 0
    r = 20
    isLatched = False
    id = 0

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
    
def makeSushi(x,y,id):
    objeto = Sushi(x,y,id)
    return objeto

def printSushis(sushiArr, correctOrder):
    for sushi in sushiArr:
        if sushi.id == 1: sushiImg = sushiImg1
        if sushi.id == 2: sushiImg = sushiImg2
        if sushi.id == 3: sushiImg = sushiImg3
        if sushi.id == 4: sushiImg = sushiImg4
        if sushi.id == 5: sushiImg = sushiImg5
        if sushi.id == 6: sushiImg = sushiImg6

        hSushi,wSushi, _ = sushiImg.shape

        if not debugMode:
            for y in range(hSushi):
                    for x in range(wSushi):                
                        if sushiImg[y,x][3] != 0 and 0<=(int(sushi.x + x - wSushi/2))<width and 0<=(int(sushi.y + y - hSushi/2))<height :
                            img[int(sushi.y + y - hSushi/2), int(sushi.x + x - wSushi/2)] = sushiImg[y,x][:3]
        else: cv2.circle(img,(sushi.x,sushi.y), 20, (40*sushi.id,40*sushi.id,40*sushi.id),-1)

    index = 0
    for sushi in correctOrder:
        
        if sushi.id == 1: sushiImg = sushiImg1
        if sushi.id == 2: sushiImg = sushiImg2
        if sushi.id == 3: sushiImg = sushiImg3
        if sushi.id == 4: sushiImg = sushiImg4
        if sushi.id == 5: sushiImg = sushiImg5
        if sushi.id == 6: sushiImg = sushiImg6

        hSushi,wSushi, _ = sushiImg.shape
        if not debugMode:
            for y in range(hSushi):
                    for x in range(wSushi):                
                        if sushiImg[y,x][3] != 0:
                            img[int((height/8) + y - hSushi/2), int(50+index*wSushi + x - wSushi/2)] = sushiImg[y,x][:3]
        else: cv2.circle(img,(int(200+index*25),int(height/8)), 20, (40*sushi.id,40*sushi.id,40*sushi.id),-1)
        
        index+=1

def checkPlateOrder(sushiArr, correctOrder, plateBounds1, plateBounds2):
    currentOrder = []
    for sushi in sushiArr:
        if plateBounds1[0] <= sushi.x <= plateBounds2[0] and plateBounds1[1] <= sushi.y <= plateBounds2[1]:
            currentOrder.append(sushi)
            currentOrder = sorted(currentOrder, key=lambda obj: obj.x)

    if len(correctOrder) != len(currentOrder):
        return False
    
    for i in range(len(correctOrder)):
        print(len(currentOrder), i, currentOrder[i].id, correctOrder[i].id)
        if currentOrder[i].id != correctOrder[i].id: return False

    return True


'''Variáveis de jogo'''
random.seed(datetime.now().timestamp())

SushisArr = []
correctOrderArr = []
#SushisArr.append(makeSushi(200,200,20,"1"))
#SushisArr.append(makeSushi(400,400,25,"1"))

playingState = True

debugMode = True
plateBounds1, plateBounds2 = None, None

points = 0


'''Variáveis de captura e renderização'''
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
prevHandLatched = False

sushiImg1 = cv2.imread('Projeto 1\Assets\sushi01.png', cv2.IMREAD_UNCHANGED) 
sushiImg2 = cv2.imread('Projeto 1\Assets\sushi02.png', cv2.IMREAD_UNCHANGED) 
sushiImg3 = cv2.imread('Projeto 1\Assets\sushi03.png', cv2.IMREAD_UNCHANGED) 
sushiImg4 = cv2.imread('Projeto 1\Assets\sushi04.png', cv2.IMREAD_UNCHANGED) 
sushiImg5 = cv2.imread('Projeto 1\Assets\sushi05.png', cv2.IMREAD_UNCHANGED) 
sushiImg6 = cv2.imread('Projeto 1\Assets\sushi06.png', cv2.IMREAD_UNCHANGED) 

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
    midPx, midPy = None, None 
    handLatched = False

    '''Lógica de jogo'''
    if playingState:
        plateBounds1 = (int(width/4),int(height/2))
        plateBounds2 = (int(3/4 * width),int(height * 3/4))
        if len(SushisArr) == 0:
            for i in range(4):
                posX = random.randint(int(width/8),int(7/8*width))
                posY = random.randint(int(6*height/8),int(7*height/8))
                id = random.randint(1,6)
                SushisArr.append(makeSushi(posX,posY,id))
            correctOrderArr = SushisArr
            random.shuffle(correctOrderArr)

        if checkPlateOrder(SushisArr,correctOrderArr, plateBounds1, plateBounds2):
            points += 100
            SushisArr = []

        

    '''Detecção de mãos e operações com indicador e polegar'''
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
                if debugMode: cv2.circle(img,(midPx,midPy),10,(255,255,255),-1)
            else: handLatched = False

    '''Movimentação de objetos com base na detecção de clique'''       
    for objeto in SushisArr:
        if handLatched: #condição de clique
            distC = np.sqrt((midPx-objeto.x)**2 + (midPy-objeto.y)**2)
            if distC < 80 or objeto.isLatched:
                objeto.isLatched = True
                objeto.x = midPx
                objeto.y = midPy
                break
        else: objeto.isLatched = False    

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    prevHandLatched = handLatched

    cv2.putText(img, str(points), (int(width/2 - 50),70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3)

    printSushis(SushisArr, correctOrderArr)
    cv2.rectangle(img,plateBounds1,plateBounds2,(0,0,0),3,1)

    if debugMode: cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    
    cv2.imshow('Image',img)

    key = 0xFF & cv2.waitKey(1)

    if key == ord('q'):
        debugMode = True
    if key == ord('w'):
        debugMode == False

    if key == 27:
        break

cap.release()
#cv2.waitKey(0)
cv2.destroyAllWindows()