FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

CMD ["python", "system_performance_consumer.py"]
