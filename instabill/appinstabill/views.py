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
from pydub import AudioSegment
from io import BytesIO

# clave de API de Google Cloud
API_KEY = config("API_KEY")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config("GOOGLE_APPLICATION_CREDENTIALS")

class SpeechToTextAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtner el archivo de audio desde la petición
        audio_file = request.FILES.get("audio")

        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        # Leer el archivo de audio en formato WAV
        audio_segment = AudioSegment.from_file(audio_file)

        # Verifica si el audio tiene más de 1 canal (estéreo) y convierte a mono
        if audio_segment.channels > 1:
            audio_segment = audio_segment.set_channels(1)

        # Asegura de que el archivo está en formato de 16 bits por muestra
        if audio_segment.sample_width != 2:  # 2 bytes = 16 bits
            audio_segment = audio_segment.set_sample_width(2)

        # Convertir el archivo a un formato que Google Cloud Speech-to-Text pueda usar
        mono_audio = BytesIO()
        audio_segment.export(mono_audio, format="wav")
        mono_audio.seek(0)  # Restablece el puntero al inicio del archivo

        # Inicializa el cliente de Google Cloud Speech-to-Text
        client = speech.SpeechClient()

        # Lee el contenido del archivo de audio ya convertido
        audio_content = mono_audio.read()

        # Configura la solicitud de reconocimiento de voz
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="es-ES",  # Idioma español
        )

        # Enviar la solicitud LongRunningRecognize para audios más largos
        operation = client.long_running_recognize(config=config, audio=audio)

        # Espera a que la operación se complete
        response = operation.result(timeout=90)  # Ajusta el timeout según sea necesario

        # Procesa la respuesta
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript

        # Devuelve la transcripción en la respuesta
        return Response({"transcription": transcription})


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
