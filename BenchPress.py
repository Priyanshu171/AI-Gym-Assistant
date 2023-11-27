import imp
import cv2
import numpy as np
import time
import PoseModule as pm
import pyttsx3
import threading

# cap = cv2.VideoCapture("BenchPress3.mp4")
cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
complete = 0

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280,720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, 11, 13, 15)
        detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        #angle = detector.findAngle(img, 11, 13, 15,False)
        per = np.interp(angle, (55, 170), (0, 100))
        bar = np.interp(angle, (55, 170), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
                complete = 0
            elif dir==0 and complete==1:
                print("wrong")
                complete = 0
                # engine.say('lift the bar up till chest')
                # engine.runAndWait()
                warning_thread = threading.Thread(target=speak, args=('lift the bar completely',))
                warning_thread.start()

        if per>=25 and per<=75:
            # print("hello")
            complete = 1

        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
                complete = 0
            elif dir==1 and complete==1:
                print("wrong")
                complete = 0
                # engine.say('release the bar down till hips')
                # engine.runAndWait()
                warning_thread = threading.Thread(target=speak, args=('release the bar down till chest',))
                warning_thread.start()

        # print(count)

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)