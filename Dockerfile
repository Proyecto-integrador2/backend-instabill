FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* 
WORKDIR /instabill/
COPY requirements.txt /instabill/
RUN pip install -r requirements.txt
COPY instabill /instabill/
