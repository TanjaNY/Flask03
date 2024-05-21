# Verwenden Sie ein offizielles Python-Laufzeitimage als Basisimage
FROM python:3.9-slim

# Legen Sie das Arbeitsverzeichnis im Container auf /python-docker fest
WORKDIR /python-docker

# Kopieren Sie die Abhängigkeitsdatei
COPY requirements.txt requirements.txt

# Installieren Sie Abhängigkeiten
RUN pip3 install -r requirements.txt

# Kopieren Sie den Anwendungscode
COPY . .

# Einrichten der SQLite-Datenbank
RUN apt-get update && apt-get install -y sqlite3
RUN mkdir -p /python-docker && sqlite3 /python-docker/app.db

# Korrigierte CMD-Anweisung
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5005"]
