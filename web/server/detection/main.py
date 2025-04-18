import mediapipe as mp
import cv2
from django.conf import settings

from .plank import PlankDetection
from .bicep_curl import BicepCurlDetection
from .squat import SquatDetection
from .lunge import LungeDetection
from .utils import rescale_frame

# Drawing helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

EXERCISE_DETECTIONS = None


def load_machine_learning_models():
    """Load all machine learning models"""
    global EXERCISE_DETECTIONS

    if EXERCISE_DETECTIONS is not None:
        return

    print("Loading ML models ...")
    EXERCISE_DETECTIONS = {
        "plank": PlankDetection(),
        "bicep_curl": BicepCurlDetection(),
        "squat": SquatDetection(),
        "lunge": LungeDetection(),
    }


def pose_detection(
    video_file_path: str, video_name_to_save: str, rescale_percent: float = 40
):
    """Pose detection with MediaPipe Pose

    Args:
        video_file_path (str): path to video
        video_name_to_save (str): path to save analyzed video
        rescale_percent (float, optional): Percentage to scale back from the original video size. Defaults to 40.

    """
    cap = cv2.VideoCapture(video_file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * rescale_percent / 100)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * rescale_percent / 100)
    size = (width, height)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    save_to_path = f"{settings.MEDIA_ROOT}/{video_name_to_save}"
    out = cv2.VideoWriter(save_to_path, fourcc, fps, size)

    print("PROCESSING VIDEO ...")
    with mp_pose.Pose(
        min_detection_confidence=0.8, min_tracking_confidence=0.8
    ) as pose:
        while cap.isOpened():
            ret, image = cap.read()

            if not ret:
                break

            image = rescale_frame(image, rescale_percent)

            # Recolor image from BGR to RGB for mediapipe
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            # Recolor image from BGR to RGB for mediapipe
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(244, 117, 66), thickness=2, circle_radius=2
                ),
                mp_drawing.DrawingSpec(
                    color=(245, 66, 230), thickness=2, circle_radius=1
                ),
            )

            out.write(image)

    print(f"PROCESSED, save to {save_to_path}.")
    return

def exercise_detection_real_time(pose_landmarks, exercise_type, image, timestamp):
    exercise_detection = EXERCISE_DETECTIONS.get(exercise_type)
    if not exercise_detection:
        raise Exception("Not supported exercise.")

    # Process the pose landmarks
    feedback = exercise_detection.detect(pose_landmarks, image, timestamp)
    return feedback

def exercise_detection(
    video_file_path: str,
    video_name_to_save: str,
    exercise_type: str,
    rescale_percent: float = 40,
) -> dict:
    """Analyzed Exercise Video

    Args:
        video_file_path (str): path to video
        video_name_to_save (str): path to save analyzed video
        exercise_type (str): exercise type
        rescale_percent (float, optional): Percentage to scale back from the original video size. Defaults to 40.

    Raises:
        Exception: Not supported exercise type

    Returns:
        dict: Dictionary of analyzed stats from the video
    """
    exercise_detection = EXERCISE_DETECTIONS.get(exercise_type)
    if not exercise_detection:
        raise Exception("Not supported exercise.")

    cap = cv2.VideoCapture(video_file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * rescale_percent / 100)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * rescale_percent / 100)
    size = (width, height)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    saved_path = f"{settings.MEDIA_ROOT}/{video_name_to_save}"
    out = cv2.VideoWriter(saved_path, fourcc, fps, size)

    print("PROCESSING VIDEO ...")
    with mp_pose.Pose(
        min_detection_confidence=0.8, min_tracking_confidence=0.8
    ) as pose:
        while cap.isOpened():
            ret, image = cap.read()

            if not ret:
                break

            # Calculate timestamp
            frame_count += 1
            timestamp = int(frame_count / fps)

            image = rescale_frame(image, rescale_percent)

            # Recolor image from BGR to RGB for mediapipe
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            # Recolor image from BGR to RGB for mediapipe
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                exercise_detection.detect(
                    mp_results=results, image=image, timestamp=timestamp
                )

            out.write(image)

    print(f"PROCESSED. Save path: {saved_path}")

    processed_results = exercise_detection.handle_detected_results(
        video_name=video_name_to_save
    )
    exercise_detection.clear_results()
    return processed_results