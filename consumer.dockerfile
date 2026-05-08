#FROM python:3.10
#WORKDIR /app
#COPY consumer.py .
#RUN pip install kafka-python pymongo
#CMD ["python", "consumer.py"]


FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py .

CMD ["python", "-u", "consumer.py"]