from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import base64
import os, sys
import numpy as np
import cv2
import mediapipe as mp
from dotenv import load_dotenv
import time

load_dotenv()


from server.detection.main import load_machine_learning_models, exercise_detection_real_time, EXERCISE_DETECTIONS

app = FastAPI()
print("PYTHONPATH:", os.getenv("PYTHONPATH"))
print("DJANGO_SETTINGS_MODULE:", os.getenv("DJANGO_SETTINGS_MODULE"))

# Configure CORS (important for browser security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or list your specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Load machine learning models on startup
    global EXERCISE_DETECTIONS
    load_machine_learning_models()

@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}

@app.websocket("/api/video/ws/exercise-detection/")
async def websocket_endpoint(websocket: WebSocket, exercise_type: str):
    await websocket.accept()
    try:
        print(f"Client connected for exercise: {exercise_type}")

        while True:
            # Receive data
            data = await websocket.receive_text()
            print(f"Data received: {data[:100]}...")  # Print the first 100 characters for brevity

            # Decode the image data
            header, encoded = data.split(",", 1)
            image_data = base64.b64decode(encoded)
            print(f"Decoded image data length: {len(image_data)}")

            # Convert image data to OpenCV format
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Calculate timestamp
            timestamp = time.time()

            # Perform pose detection with MediaPipe
            try:
                with mp.solutions.pose.Pose(
                    min_detection_confidence=0.5, min_tracking_confidence=0.5
                ) as pose:
                    results = pose.process(frame)

                    if results.pose_landmarks:
                        print("FastAPI: Pose landmarks detected")
                        # Perform exercise detection
                        feedback = exercise_detection_real_time(results.pose_landmarks, exercise_type, frame, timestamp)
                        print(f"Feedback generated: {feedback}")
                        feedback_message = " ".join(feedback)

                        # Send feedback
                        feedback = {"feedback": feedback_message}
                        print(f"Sending feedback: {feedback}")
                        await websocket.send_json(feedback)
                    else:
                        print("FastAPI: No pose landmarks detected")
            except Exception as e:
                print(f"Error during pose detection: {e}")

    except WebSocketDisconnect:
        print(f"Client disconnected for exercise: {exercise_type}")
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)