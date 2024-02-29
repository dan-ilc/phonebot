# Go as small as possible
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY twilio_client.py run.sh .
COPY webapp/build frontend

CMD ["python3", "twilio_client.py"]
