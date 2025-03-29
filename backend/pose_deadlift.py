import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm

def deadlift():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "ADJUST YOUR FORM"

    with detector.pose:
        while True:
            ret, img = cap.read()
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)

            if len(lmList) != 0:
                hip_angle = detector.findAngle(img, 11, 23, 25)  # Shoulder-Hip-Knee
                back_angle = detector.findAngle(img, 11, 23, 11)  # Shoulder-Hip-Shoulder
                knee_angle = detector.findAngle(img, 23, 25, 27)  # Hip-Knee-Ankle

                # Hand position (bar path)
                wrist_shin_dist = np.linalg.norm(
                    np.array([lmList[15][1], lmList[15][2]]) - np.array([lmList[27][1], lmList[27][2]])
                )

                # Percentage of deadlift completion
                per = np.interp(hip_angle, (60, 180), (0, 100))
                bar = np.interp(hip_angle, (60, 180), (380, 50))

                # Check form
                if back_angle > 160 and back_angle < 180 and knee_angle > 160:
                    if wrist_shin_dist < 50:  # Ensure hands stay close to the body
                        form = 1
                    else:
                        feedback = "KEEP HANDS CLOSE TO LEGS"
                else:
                    feedback = "KEEP YOUR BACK STRAIGHT"

                # Deadlift count logic
                if form == 1:
                    if per == 100:
                        feedback = "LOCKOUT"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    if per == 0:
                        feedback = "LOWER THE BAR"
                        if direction == 1:
                            count += 0.5
                            direction = 0

                # Draw bar
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (950, 230), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                # Deadlift counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

                # Feedback
                cv2.putText(img, feedback, (150, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                # Convert frame to JPEG
                ret, jpeg = cv2.imencode('.jpg', img)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# Let me know if you want to fine-tune the feedback or add more accuracy checks! 🚀
