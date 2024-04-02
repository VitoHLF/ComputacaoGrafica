import numpy as np
import cv2 as cv
import time

#ISSO É UM EXEMPLO

cap = cv.VideoCapture('moedas.mp4')
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    time.sleep(0.05)

    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    if cv.waitKey(1) == ord('q'):
        break

    gray = cv.bilateralFilter(gray, 9,75,75)
    gray = cv.blur(gray,(5,5))

    circles = []
    circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,180, param1=80, param2=50,minRadius=50,maxRadius=400)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        previous = circles[0][0]

        for i in circles[0,:]:
            cv.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            cv.circle(frame,(i[0],i[1]),2,(0,0,255),3)

            cv.line(frame,(i[0],i[1]),(previous[0], previous[1]), (255,0,0), 4)
            previous = i
        

    cv.imshow('frame',frame)
    

cap.release()
cv.destroyAllWindows()


    
