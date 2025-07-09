#!/bin/sh

# Dieses Skript wartet, bis die PostgreSQL-Datenbank bereit ist,
# führt dann die Migrationen aus und startet schließlich die Anwendung.

# Die Umgebungsvariablen werden aus der .env-Datei geladen, die in docker-compose.yml
# für den Web-Service angegeben ist.
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Warte auf Postgres unter ${DB_HOST}:${DB_PORT}..."

# Wir verwenden ein kleines Python-Skript, um die DB-Verbindung zu prüfen,
# da netcat im python:3.11-slim-Image nicht installiert ist.
python << END
import socket
import time
import os

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", 5432))

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            break
    except OSError:
        time.sleep(1)
print("Postgres ist bereit!")
END

echo "Führe Datenbank-Migrationen aus..."
python manage.py migrate

# Führe den Befehl aus, der an dieses Skript übergeben wurde (z.B. gunicorn)
exec "$@"