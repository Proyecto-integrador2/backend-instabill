from django.urls import path
from .views import SpeechToTextAPIView

urlpatterns = [
    path('speech-to-text/', SpeechToTextAPIView.as_view(), name='speech-to-text'),
]
