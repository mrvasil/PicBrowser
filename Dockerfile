FROM mirror.gcr.io/python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y exiftool && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 20191

CMD ["python", "run.py"]