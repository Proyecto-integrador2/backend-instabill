from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from decouple import config

# clave de API de Google Cloud
API_KEY = config('API_KEY')

class SpeechToTextAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Verificar que se haya enviado un archivo de audio
            if 'audio' not in request.FILES:
                return Response({"error": "No se proporcionó un archivo de audio."}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el archivo de audio
            audio_file = request.FILES['audio']
            audio_content = audio_file.read()

            # Codificar el audio en base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')

            # Definir la URL de la API de Google Cloud Speech-to-Text
            url = f"https://speech.googleapis.com/v1/speech:recognize?key={API_KEY}"

            # Configuración para la solicitud a Google Cloud
            headers = {
                "Content-Type": "application/json"
            }

            # Configuración de la solicitud de transcripción
            data = {
                "config": {
                    "encoding": "WAV",  # Formato
                    "sampleRateHertz": 16000,  # Tasa de muestreo de archivo de audio
                    "languageCode": "es-ES"  # Idioma 
                },
                "audio": {
                    "content": audio_base64
                }
            }

            # Hacer la solicitud a la API de Google
            response = requests.post(url, headers=headers, json=data)

            # Verificar si la solicitud fue exitosa
            if response.status_code != 200:
                return Response({"error": "Error en la solicitud a Google Cloud Speech-to-Text."}, status=response.status_code)

            # Extraer la transcripción del JSON de respuesta
            transcription_data = response.json()
            transcription = ""
            for result in transcription_data.get("results", []):
                transcription += result["alternatives"][0]["transcript"]

            return Response({"transcription": transcription}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
