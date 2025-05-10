from django.urls import path

from .input import Base64InputView

urlpatterns = [
    path('base64input/', Base64InputView.as_view()),
]
