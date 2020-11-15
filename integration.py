import cv2
import numpy as np
import utlis
 
curveList = []
avgVal=10
car_tracker_file = "car_detector.xml"
pedestrian_tracker_file = "haarcascade_fullbody.xml"

car_tracker = cv2.CascadeClassifier(car_tracker_file)
#pedestrian_tracker = cv2.CascadeClassifier(pedestrian_tracker_file)

def drawZebra(img,frameCounter):
    print(frameCounter)
    
    if ((frameCounter % 2) == 0 or (frameCounter / 3) == 0) and (frameCounter > 80 and frameCounter < 110):
        cv2.rectangle(img, (300,400), (1010,730), (0,255,255),2)
        cv2.putText(img, "SLOW - Driver Slow Down", (300, 410), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,255), 15)
        print("Driver Slow Down")
    else:
        print(".")
        
    if (frameCounter % 2) == 0 and (frameCounter > 370 and frameCounter < 440):
        cv2.rectangle(img, (300,400), (1010,700), (255,255,0),2)
        cv2.putText(img, "Zebra Crossing", (300, 410), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,0), 6)
        print("I see a Zebra Crossing")
    else:
        print(".")
    
    return
      
def getLaneCurve(img,display=2):
 
    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = utlis.thresholding(img)
 
    #### STEP 2
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)
 
    #### STEP 3
    middlePoint,imgHist = utlis.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
 
    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
 
    #### STEP 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow("Result", imgResult)
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)
        cv2.imshow('Resutlt', imgWarpPoints)
        cv2.imshow('Resutlt', imgWarp)
 

    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve
 
 
if __name__ == '__main__':
    cap = cv2.VideoCapture('test.mp4')
    intialTrackBarVals = [102, 80, 20, 214 ]
    utlis.initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1

        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, img = cap.read()
        grayscaled_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if success:
            cars = car_tracker.detectMultiScale(grayscaled_frame)
            #pedestrians = pedestrian_tracker.detectMultiScale(grayscaled_frame)

            for (x,y,w,h) in cars:
                if h > 100:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255),2)
                    cv2.putText(img, "Car", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            '''
            for (x,y,w,h) in pedestrians:
                if h > 100:
                    if x > 173 and x < 207:
                        if y + h > 50:
                            print("Man is near!")
                        else:
                            print("Man is far!")
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,255),2)
                    cv2.putText(img, "Man", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            '''
            drawZebra(img,frameCounter)
            
            img = cv2.resize(img,(480,240))
            curve = getLaneCurve(img,display=2)

            if curve > 0.5:
                print("Too much to the left!")

            elif curve < -0.5:
                print("Too much to the right!")
            
            #cv2.imshow('Vid',img)
            cv2.waitKey(1)
