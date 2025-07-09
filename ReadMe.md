# ICD10 API

Dieses Projekt stellt eine API zur Verfügung, die ICD-10-Codes und Diagnosen verwaltet. 
Es basiert auf Django und verwendet Docker für die Containerisierung und beinhaltet eine PostgreSQL DB.
## Voraussetzungen

- Python
- Django
- Docker
- Docker Compose
## Installation und Setup

### Voraussetzungen
- Eine `.env`-Datei mit den notwendigen Umgebungsvariablen muss vorhanden sein.
### .env-Datei erstellen

Kopieren Sie die Beispiel-Umgebungsdatei und passen Sie sie ggf. an:
```sh
cp .env.example .env
```

### Ports und Zugriff

- Die API ist nach dem Start unter [http://localhost:9000](http://localhost:9000) erreichbar.
- Das Django Admin-Interface finden Sie unter [http://localhost:9000/admin](http://localhost:9000/admin).

### ICD-10 Datensätze

Die ICD-10-Codes können  heruntergeladen werden [BfArM](https://www.bfarm.de/DE/Medizinprodukte/Klassifikationen/ICD10-GM/_node.html). Diese Daten dienen als Quelle für die Imports. Und werden mit dem Stand 07/2025 mit folgenden Schritten importiert.
### Schritte

1. **Docker-Container starten**  
Führen Sie den folgenden Befehl aus, um die Container zu starten:
    ```sh
    docker-compose up -d
    ```

2. **Datenbank migrieren**  
    Bevor Sie die ICD-10-Codes importieren, müssen Sie die Datenbank migrieren:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

3. **ICD-10-Codes importieren**  
    Führen Sie nach dem Start der Container folgenden Befehl aus, um die ICD-10-Codes zu importieren:
    ```sh
    docker-compose exec web python manage.py import_icd_codes
    ```


4. **Diagnosen importieren**  
    Importieren Sie anschließend die Diagnosen mit:
    ```sh
    docker-compose exec web python manage.py import_diagnoses
    ```

4. **Optional**  
    superuser erstellen:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

