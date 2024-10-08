import os
from .models import Bill
from .serializers import BillSerializer
from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from decouple import config
from google.cloud import speech


# clave de API de Google Cloud
API_KEY = config("API_KEY")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config("GOOGLE_APPLICATION_CREDENTIALS")


class SpeechToTextAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtén el archivo de audio desde la petición
        audio_file = request.FILES.get("audio")

        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        # Inicializa el cliente de Google Cloud Speech-to-Text
        client = speech.SpeechClient()

        # Lee el archivo de audio
        audio_content = audio_file.read()

        # Configura la solicitud
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Cambiar según el formato del archivo
            sample_rate_hertz=48000,  # Ajusta según el archivo
            language_code="es-ES",  # Idioma de transcripción (español)
        )

        # Envía la solicitud a la API de Google
        response = client.recognize(config=config, audio=audio)

        # Procesa la respuesta
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript

        # Devuelve la transcripción en la respuesta
        return Response({"transcription": transcription})


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
