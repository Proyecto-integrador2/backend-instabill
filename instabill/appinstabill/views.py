import os
from .models import Factura
from .serializers import FacturaSerializer
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
    """
    API View que permite la transcripción de archivos de audio a texto utilizando Google Cloud Speech-to-Text.

    Esta vista acepta una solicitud HTTP POST que contiene un archivo de audio y procesa dicho archivo para convertirlo en texto.
    El archivo de audio se valida y se convierte a un formato compatible antes de ser enviado al servicio de Google Cloud para
    su transcripción.

    Methods:
        post(request, *args, **kwargs):
            Procesa el archivo de audio enviado en la solicitud POST, lo convierte a un formato compatible y utiliza Google Cloud 
            Speech-to-Text para transcribir el audio a texto.

    Requisitos:
        - Google Cloud Speech-to-Text configurado en el entorno (autenticación mediante las credenciales del servicio).
        - La librería `pydub` para el procesamiento de audio.
        - ffmpeg o avconv instalado en el servidor para la manipulación de archivos de audio.

    Endpoint:
        POST /speech-to-text/
        
    Request:
        - Formato: multipart/form-data
        - Parámetro obligatorio: `audio` (archivo de audio en formato .wav, .mp3, .ogg, etc.)

    Ejemplo de uso:
        Enviar una solicitud POST con un archivo de audio:
        ```
        curl -X POST http://127.0.0.1:8000/speech-to-text/ \
        -F "audio=@mi_archivo_audio.wav"
        ```
    """

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


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
