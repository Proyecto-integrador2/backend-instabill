from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpeechToTextAPIView, FacturaViewSet

router = DefaultRouter()
router.register(r"bills", FacturaViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("speech-to-text/", SpeechToTextAPIView.as_view(), name="speech-to-text"),
]
