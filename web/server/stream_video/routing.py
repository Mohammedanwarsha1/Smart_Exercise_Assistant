from django.urls import path
from .consumers import ExerciseDetectionConsumer

websocket_urlpatterns = [
    path("api/video/ws/exercise-detection/", ExerciseDetectionConsumer.as_asgi()),
]