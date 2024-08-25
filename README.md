# Von Entwicklung zu Produktion


### 1. Code Refactoring

**Warum brauchen wir Code Refactoring?**
Code-Refactoring ist aus mehreren Gründen wichtig:

1.Verbesserte Lesbarkeit: Macht den Code verständlicher für Entwickler.
2.Erhöhte Wartbarkeit: Erleichtert zukünftige Änderungen und Fehlerbehebungen.
3.Effizienzsteigerung: Optimiert die Leistung und reduziert Redundanzen.
4.Bessere Skalierbarkeit: Ermöglicht einfachere Erweiterungen.
5.Reduzierte technische Schulden: Verhindert Anhäufung von Problemen.
-Verbesserte Testbarkeit: Erleichtert das Schreiben und Ausführen von Tests.
-Anpassung an neue Standards: Hält den Code auf dem neuesten Stand.
-Beseitigung von "Code-Geruch": Entfernt schlechte Praktiken und Muster.
-Förderung der Wiederverwendbarkeit: Ermöglicht die Nutzung von Code in anderen Projekten.

**Änderung:**
In der zweiten Version wurde eine umfassende Logging-Einrichtung mit dem `logging`-Modul hinzugefügt, die sowohl File- als auch Console-Handler umfasst. Logs werden in `/tmp/flask.log` gespeichert.

**Warum ist Logging wichtig?**
Logging ist entscheidend für Produktionsumgebungen, da es dabei hilft, Fehler zu erkennen, die Leistung zu überwachen und den Zustand der Anwendung nachzuvollziehen. Durch detailliertes Logging können Probleme schneller identifiziert und behoben werden.

**Code:**

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler('/tmp/flask.log', maxBytes=1024 * 1024 * 10, backupCount=10)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
```

### 2. AWS Lambda-Unterstützung

**Deployment-Reafactoring**


**Änderung:**
Die zweite Version enthält die `awsgi`-Bibliothek und eine auskommentierte Lambda-Handler-Funktion.

**Warum AWS Lambda?**
AWS Lambda ermöglicht das Ausführen von Code ohne die Verwaltung von Servern. Es ist eine kosteneffiziente und skalierbare Option für den Einsatz von Anwendungen in der Cloud.

**Code:**

```python
import awsgi

# Lambda handler function
# def lambda_handler(event, context):
#    logger.info("Lambda function invoked")
#    return awsgi.response(app, event, context)
```

### 3. Fehlerbehandlung

**Änderung:**
Die zweite Version fügt eine Fehlerbehandlung mit Logging für die Datenbankverbindung, Tabellenerstellung und Flask-Routen hinzu. Fehlerseiten werden angezeigt, wenn Ausnahmen auftreten.

**Warum Fehlerbehandlung?**
Durch robuste Fehlerbehandlung und das Anzeigen von Fehlerseiten wird die Benutzerfreundlichkeit verbessert und es wird sichergestellt, dass die Anwendung stabil bleibt, selbst wenn Fehler auftreten.

**Code:**

```python
def get_db_connection():
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        logger.info("Database connection established successfully")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM calculations ORDER BY timestamp DESC')
        results = cursor.fetchall()
        logger.info("Retrieved calculation results for index page")
        return render_template('index.html', results=results)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template('error.html', error="An error occurred while fetching data"), 500
    finally:
        conn.close()
```

### 4. Datenbankpfadänderung

**Änderung:**
Der Datenbankpfad wurde von `os.getcwd()` auf `/tmp` geändert.

**Warum der Wechsel zu `/tmp`?**
Das Verzeichnis `/tmp` ist für temporäre Dateien vorgesehen und eignet sich gut für Anwendungen, die in containerisierten oder serverlosen Umgebungen ausgeführt werden, wie z.B. AWS Lambda.

**Code:**

```python
BASE_DIR = '/tmp'
db_path = os.path.join(BASE_DIR, "circle_calculations.db")
```

### 5. Änderungen im Ausführungsablauf

**Änderung:**
Die zweite Version entfernt die Datenbankverbindung und Tabellenerstellung aus dem Block `if __name__ == '__main__'` und fügt sie separat hinzu. Das `app.run()`-Aufruf wurde ebenfalls geändert.

**Warum die Änderung?**
Dies stellt sicher, dass die Tabellenerstellung unabhängig von der Art der Ausführung der Anwendung erfolgt und verbessert die Struktur des Codes.

**Code:**

```python
# Create the table on first execution
create_table()

if __name__ == '__main__':
    app.run(debug=True)
```

## Zusammenfassung

Diese Änderungen verbessern die Wartbarkeit, Fehlerdiagnose und Cloud-Bereitschaft der Anwendung erheblich. Logging und robuste Fehlerbehandlung sind wesentliche Bestandteile einer Produktionsumgebung, und die Unterstützung für AWS Lambda bietet eine skalierbare Bereitstellungsoption. Der Wechsel des Datenbankpfads zu `/tmp` und die Anpassungen im Ausführungsablauf tragen dazu bei, dass die Anwendung in verschiedenen Umgebungen konsistent und zuverlässig läuft.
