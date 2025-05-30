import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

def right_curl():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "LOWER YOUR ARM"

    with detector.pose:
        while True:
                
            ret, img = cap.read() #640 x 480


            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            # print(lmList)
            if len(lmList) != 0:
                elbow = detector.findAngle(img, 12, 14, 16)
                shoulder = detector.findAngle(img, 14, 12, 24)

                #Percentage of success of curl
                per = np.interp(elbow, (40, 160), (100, 0))
                
                #Bar to show curl progress
                bar = np.interp(elbow, (40, 160), (50, 380))

                #Check to ensure right form before starting the program
                if shoulder < 40:
                    form = 1

                #Check for full range of motion for the pushup
                if form == 1:
                    if per == 0:
                        if elbow > 160 and shoulder < 40:
                            feedback = "UP"
                            if direction == 0:
                                count += 0.5
                                direction = 1
                        else:
                            feedback = "LOWER YOUR ARM"
                            
                    if per == 100:
                        if elbow < 40 and shoulder < 40:
                            feedback = "DOWN"
                            if direction == 1:
                                count += 0.5
                                direction = 0
                        else:
                            feedback = "LOWER YOUR ARM"
                                # form = 0

                print(count)
                
                #Draw Bar
                if form == 1:
                    cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                    cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 0), 2)


                #Pushup counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                            (255, 0, 0), 5)
                
                #Feedback 
                
                cv2.putText(img, feedback, (150, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                            (0, 0, 255), 2)

                
            # Convert the frame to JPEG format
                ret, jpeg = cv2.imencode('.jpg', img)

                # Yield the frame as a bytes-like object
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')