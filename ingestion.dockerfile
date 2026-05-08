#FROM python:3.10
#WORKDIR /app
#COPY ingestion.py .
#RUN pip install kafka-python requests
#CMD ["python", "ingestion.py"]

FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion.py .

CMD ["python", "-u", "ingestion.py"]