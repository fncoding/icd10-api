# Basis-Image mit Python
FROM python:3.11-slim

# Umgebungsvariablen setzen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere die Abhängigkeiten
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Projektcode
COPY . /app/

# Mache das Entrypoint-Skript ausführbar
RUN chmod +x /app/entrypoint.sh

# Port 9000 freigeben
EXPOSE 9000

# Setze das Entrypoint-Skript
ENTRYPOINT ["/app/entrypoint.sh"]

# Standardbefehl zum Starten der Anwendung (wird an das Entrypoint-Skript übergeben)
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "backend.wsgi:application"]