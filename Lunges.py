import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
r_count = 0
l_count = 0
r_dir=0
l_dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280,720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    track=1
    if len(lmList) != 0:
        # Right leg goes first
        angle_r = detector.findAngle(img, 24, 26, 28)
        angle_l = detector.findAngle(img, 23, 25, 27)
        r_per = np.interp(angle_r, (80, 170), (0, 100))
        r_bar = np.interp(angle_r, (55, 165), (650, 100))
        # Then goes the lest leg

        l_per = np.interp(angle_l, (80, 170), (0, 100))
        l_bar = np.interp(angle_l, (55, 165), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        color = (255, 0, 255)
        if r_per == 100:
            color = (0, 255, 0)
            if r_dir == 0:
                r_count += 0.5
                r_dir = 1
        if r_per == 0:
            color = (0, 255, 0)
            if r_dir == 1:
                r_count += 0.5
                r_dir = 0

        if l_per == 100:
            color = (0, 255, 0)
            if l_dir == 0:
                l_count += 0.5
                l_dir = 1
        if l_per == 0:
            color = (0, 255, 0)
            if l_dir == 1:
                l_count += 0.5
                l_dir = 0

        print(r_count)
        print(l_count)

        # Draw Right Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(r_bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(r_per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 3,
                    color, 4)
        cv2.putText(img, "Right", (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, 4)

        # Draw Left Bar
        cv2.rectangle(img, (100, 100), (175, 650), color, 3)
        cv2.rectangle(img, (100, int(l_bar)), (175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(l_per)} %', (100, 75), cv2.FONT_HERSHEY_PLAIN, 3,
                    color, 4)
        cv2.putText(img, "Left", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    color, 4)

        # Draw Right Lunge Count
        cv2.rectangle(img, (1100, 1550), (1350, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(r_count)), (1045, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

        # Draw Left Lunge Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(l_count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)