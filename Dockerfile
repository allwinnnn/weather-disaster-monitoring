#FROM python:3.10

#WORKDIR /app

#COPY . .

#RUN pip install kafka-python pymongo requests

#CMD ["python", "-u", "consumer.py"]


FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only consumer code
COPY consumer.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "consumer.py"]