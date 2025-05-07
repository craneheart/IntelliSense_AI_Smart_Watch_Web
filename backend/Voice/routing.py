from django.urls import path
from .consumer import RealTimeRecognition

websocket_urlpatterns = [
    path('recognition/', RealTimeRecognition.RealTimeRecognitionConsumer.as_asgi()),
]
