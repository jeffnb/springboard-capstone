FROM python:latest

WORKDIR /app
COPY main.py /app
COPY requirements.txt /app
COPY model_data/ /app/model_data/
COPY src/ /app/src/

RUN ls /app
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 8888

VOLUME /app

CMD ["python3", "main.py"]
