FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /compressor-fapi
WORKDIR /compressor-fapi
COPY requirements.txt /compressor-fapi/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg -y

COPY . /compressor-fapi
CMD ["fastapi", "dev", "main.py"]