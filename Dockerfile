FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg -y

COPY . .
CMD ["fastapi", "dev", "main.py"]