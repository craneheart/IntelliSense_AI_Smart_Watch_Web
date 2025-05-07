from django.urls import path
from channels.routing import URLRouter

from ComputingUnit import routing as computing_unit
from Voice import routing as voice

websocket_urlpatterns = [
    path('computingUnit/', URLRouter(computing_unit.websocket_urlpatterns)),
    path('voice/', URLRouter(voice.websocket_urlpatterns)),
]
