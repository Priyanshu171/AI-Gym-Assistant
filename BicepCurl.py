import cv2
import numpy as np
import time
import PoseModule as pm
import pyttsx3
import threading

# cap = cv2.VideoCapture("AdityaBicepCurl.mp4")
cap = cv2.VideoCapture(0)

engine = pyttsx3.init()

detector = pm.poseDetector()
r_count = 0
l_count = 0
l_dir = 0
r_dir = 0
complete = 0
pTime = 0
set_count=100

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle_r = detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        angle_l = detector.findAngle(img, 11, 13, 15)
        per_r = np.interp(angle_r, (210, 340), (0, 100))
        per_l = np.interp(angle_r, (210, 340), (0, 100))
        bar_l = np.interp(angle_r, (210, 340), (650, 100))
        bar_r = np.interp(angle_r, (210, 340), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        color = (255, 0, 255)

        if per_r == 0:
            color = (0, 255, 0)
            if r_dir == 1:
                r_count += 0.5
                r_dir = 0
                complete = 0
            elif r_dir==0 and complete==1:
                print("wrong")
                complete = 0
                # engine.say('lift the bar up till chest')
                # engine.runAndWait()
                warning_thread = threading.Thread(target=speak, args=('lift the bar up till chest',))
                warning_thread.start()

        if per_r>=25 and per_r<=75:
            # print("hello")
            complete = 1

        if per_r == 100:
            color = (0, 255, 0)
            if r_dir == 0:
                r_count += 0.5
                r_dir = 1
                complete = 0
            elif r_dir==1 and complete==1:
                print("wrong")
                complete = 0
                # engine.say('release the bar down till hips')
                # engine.runAndWait()
                warning_thread = threading.Thread(target=speak, args=('release the bar down till hips',))
                warning_thread.start()

        if per_l == 100:
            color = (0, 255, 0)
            if l_dir == 0:
                l_count += 0.5
                l_dir = 1
        if per_l == 0:
            color = (0, 255, 0)
            if l_dir == 1:
                l_count += 0.5
                l_dir = 0

        # print(r_count)
        # print(l_count)

        # Draw Right Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar_r)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per_r)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 3,
                    color, 4)
        cv2.putText(img, "Right", (1100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, 4)

        # Draw Left Bar
        cv2.rectangle(img, (100, 100), (175, 650), color, 3)
        cv2.rectangle(img, (100, int(bar_l)), (175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per_l)} %', (100, 75), cv2.FONT_HERSHEY_PLAIN, 3,
                    color, 4)
        cv2.putText(img, "Left", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, 4)

        # Draw Right Lunge Count
        #cv2.rectangle(img, (1100, 1550), (1350, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(r_count)), (1045, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

        # Draw Left Lunge Count
        #cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(l_count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                #(255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)