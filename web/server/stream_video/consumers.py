import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
import mediapipe as mp
from detection.main import exercise_detection_real_time

class ExerciseDetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    async def disconnect(self, close_code):
        self.pose.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            # Decode the base64 image
            image_data = base64.b64decode(text_data.split(",")[1])
            np_arr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                # Process the pose landmarks and provide feedback
                feedback = exercise_detection_real_time(results.pose_landmarks, self.scope['url_route']['kwargs']['exercise_type'])
                await self.send(text_data=json.dumps(feedback))