from django.urls import path

from .consumer import ComputingUnit

websocket_urlpatterns = [
    path('connect/', ComputingUnit.ConnectConsumer.as_asgi()),
    path('pipe/', ComputingUnit.PipeConsumer.as_asgi()),
    path('deepseek/', ComputingUnit.DeepSeekConsumer.as_asgi()),
]
