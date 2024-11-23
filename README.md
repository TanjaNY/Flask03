# Deployment- Von Entwicklung zu Produktion

## Überführung einer Entwicklungsanwendung in die Produktion

Nachdem wir die Entwicklungsphase unserer Flask-Anwendung abgeschlossen haben, müssen wir die Anwendung nun für den Einsatz in der Produktion vorbereiten. Dafür sind mehrere Anpassungen erforderlich. Wichtige Überlegungspunkte sind:

- **Debugging-Funktionen deaktivieren**: Zunächst sollten Debugging-Funktionen deaktiviert werden, um die Sicherheit und Performance zu verbessern.
                                          Das Deaktivieren des Debugging-Modus in der Produktion ist wichtig, um Sicherheitsrisiken zu vermeiden, da Debugging- 
                                          Informationen sensible Daten preisgeben können, und um die Performance der Anwendung zu verbessern. Außerdem sorgt es 
                                          für eine stabile Anwendung und eine bessere Benutzererfahrung, indem detaillierte Fehlermeldungen verborgen werden.

- **Produktionsreife Datenbank**: Die Anwendung sollte auf eine produktionsreife Datenbank umgestellt werden, die für hohe Lasten ausgelegt ist.

- **Sicherheitsmaßnahmen implementieren**: Zudem müssen Sicherheitsmaßnahmen wie HTTPS, Firewalls und Zugriffskontrollen implementiert werden.

- **Skalierbarkeit und Überwachung**: Schließlich sollten Skalierbarkeit und Überwachungstools berücksichtigt werden, um eine stabile und zuverlässige Laufzeitumgebung zu gewährleisten.

- **Webserver einrichten**: Ein Webserver ist notwendig, um die Anwendung effizient und sicher in der Produktion bereitzustellen, Anfragen zu verwalten

### 1. Code Refactoring

**Warum brauchen wir Code Refactoring?**

Code-Refactoring ist ein wichtiger Schritt im Softwareentwicklungsprozess, der dazu beiträgt, die Codequalität zu verbessern und die Bereitstellung zu erleichtern. Durch Refactoring wird der Code lesbarer, wartbarer und weniger fehleranfällig, was die Zusammenarbeit im Team und die langfristige Pflege der Software vereinfacht.Die Gründen, warum das Refactoring wichtig ist:

1. Verbesserte Lesbarkeit: Macht den Code verständlicher für Entwickler.

2. Erhöhte Wartbarkeit: Erleichtert zukünftige Änderungen und Fehlerbehebungen.

3. Effizienzsteigerung: Optimiert die Leistung und reduziert Redundanzen.

4. Bessere Skalierbarkeit: Ermöglicht einfachere Erweiterungen.

5. Reduzierte technische Schulden: Verhindert Anhäufung von Problemen.
   
6. Verbesserte Testbarkeit: Erleichtert das Schreiben und Ausführen von Tests.

7.Anpassung an neue Standards: Hält den Code auf dem neuesten Stand.

8.Beseitigung von "Code-Geruch": Entfernt schlechte Praktiken und Muster.

9.Förderung der Wiederverwendbarkeit: Ermöglicht die Nutzung von Code in anderen Projekten.

Code-Refactoring vor der Produktions-Deployment ist wichtig, um sicherzustellen, dass der Code robust und fehlerfrei ist. Es hilft, potenzielle Performance-Probleme und Sicherheitslücken zu identifizieren und zu beheben, bevor sie in einer Live-Umgebung Schaden anrichten können. Durch Refactoring wird der Code sauberer und einfacher zu verstehen, was die Wartung und das Debugging nach der Bereitstellung erleichtert. Zudem stellt es sicher, dass der Code effizient und skalierbar ist, was in einer Produktionsumgebung von entscheidender Bedeutung ist.


### 2. Datenbankinitialisierung mit dem Kontextmanager für Datenbankoperationen (`with`-Statements)


- - **Änderung**: Die Datenbankinitialisierung wird in der Funktion `init_db()` ausgeführt, die in einem Kontextmanager ausgeführt wird.Ein Kontextmanager in Python ist ein Objekt, das den Kontext für die Ausführung eines Codeblocks definiert. Es wird typischerweise mit dem with-Statement verwendet.
- **Erklärung**: Dies stellt sicher, dass die Datenbanktabelle nur einmal beim Start der Anwendung erstellt wird, falls sie noch nicht existiert. Dadurch wird die Initialisierung sauberer und robuster.

- - **Änderung**: Alle Datenbankoperationen verwenden nun `with`-Statements.
- **Erklärung**: Der Einsatz von `with`-Statements stellt sicher, dass die Datenbankverbindung automatisch geschlossen wird, auch wenn ein Fehler auftritt. Dies macht den Code sicherer und kompakter, indem es die Notwendigkeit eines `finally`-Blocks eliminiert.

**Code bevor** 

Eine neue Funktion wird erstellt.

 **Code danach** 

 ```python
def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabelle 'calculations', 
    wenn sie noch nicht vorhanden ist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS calculations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    radius REAL NOT NULL,
                    area REAL NOT NULL,
                    timestamp DATETIME NOT NULL
                )
            ''')
    except sqlite3.Error as e:
        app.logger.error(f"Database table creation error: {e}")
        raise InternalServerError("Fehler beim Erstellen der Datenbanktabelle")
```

## 3. Fehlerbehandlung und Logging

**Why Logging is Essential in Production Applications**

# Warum Logging in Produktionsanwendungen unerlässlich ist

### 3.1.1 Problemerkennung und Fehlerbehebung
- Die alte Version hatte kein Logging, was folgende Schwierigkeiten verursachte:
  - Fehlerursachen und -zeitpunkte waren schwer zu identifizieren
  - Der Anwendungsablauf konnte nicht nachverfolgt werden
  - Fehlerbehebung in der Produktion war erschwert
- Die neue Version implementiert umfassendes Logging für:
  - Datenbankverbindungsfehler
  - Probleme bei der Anfrageausführung
  - Eingabevalidierungsfehler
  - Änderungen des Anwendungszustands

### 3.2 Wichtige Verbesserungen in der neuen Version
#### 3.2.1. Logging-Konfiguration
```python
# Hinzufügen der Logging-Konfiguration
file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 10, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
```

### 3.2.2 Fehlerbehandlung und Logging
```python
# Alte Version - ohne Fehler-Logging
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Neue Version - mit Fehler-Logging
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Database connection error: {e}")
        raise InternalServerError("Datenbankverbindungsfehler")
```

## 3.3 Vorteile des neuen Logging-Systems

### 3.3.1 Log-Rotation
- Verwendet `RotatingFileHandler` zur Verwaltung der Protokolldateigröße
- Erstellt automatisch neue Protokolldateien bei Erreichen der Größenbeschränkung
- Behält 10 Sicherungsdateien bei (backupCount=10)
- Verhindert Speicherplatzprobleme durch unbegrenztes Logwachstum

### 3.3.2 Strukturiertes Log-Format
- Zeitstempel: Zeitpunkt des Ereignisses
- Name: Logger-Name (Modul/Komponente)
- Level: Schweregrad des Logs (DEBUG, INFO, ERROR, etc.)
- Nachricht: Detaillierte Beschreibung des Ereignisses

### 3.3.3 Fehlernachverfolgung
- Datenbankfehler werden nun protokolliert mit:
  - Verbindungsfehlern
  - Fehler bei der Anfrageausführung
  - Probleme bei der Tabellenerstellung
  - Fehler bei der Dateneinfügung

## 3.4. Logging-Konfigurationsdatei (logging.conf)
```ini
[loggers]
keys=root

[handlers]
keys=fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=fileHandler

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('flask.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## 3.5 Sicherheitsverbesserungen
- Debug-Modus in der Produktion deaktiviert (debug=False)
- Verbesserte Fehlerbehandlung verhindert die Offenlegung sensibler Informationen
- Logs können potenzielle Sicherheitsprobleme oder Angriffe identifizieren

## 3.6 Wartbarkeitsverbesserungen
- Separate Logging-Konfigurationsdatei
- Einheitliche Fehlerbehandlungsmuster
- Klare Trennung der Zuständigkeiten
- Verbesserte Codeorganisation

### 4. Nutzung von `math.pi`

- **Änderung**: Die Berechnung der Kreisfläche verwendet nun die Konstante `pi` aus dem `math`-Modul.
- **Erklärung**: `math.pi` ist eine genauere und standardisierte Methode zur Berechnung des Pi-Wertes, was zu präziseren Berechnungen führt. Die Auslagerung der Berechnung in die Funktion `calculate_area()` erhöht die Modularität und Wiederverwendbarkeit des Codes.

**Code bevor**  
```python
def calculate():
    try:
        radius = float(request.form['radius'])
        area = round(3.14159 * radius ** 2, 2)
```

**Code danach** 

```python
from math import pi
def calculate_area(radius):
    """
    Berechnet die Fläche eines Kreises anhand des übergebenen Radius.
    """
    return round(pi * radius ** 2, 2)

```
**Was ist passiert?**
**Eine separate Funktion wurde erstellt:**
Die Berechnung wurde in eine eigenständige Funktion namens calculate_area ausgelagert. Dies verbessert die Modularität und Wiederverwendbarkeit des Codes.

**Verwendung des math-Moduls:*
Statt den ungenauen Wert 3.14159 für Pi zu verwenden, wird nun die Konstante pi aus dem math-Modul importiert. Dies erhöht die Genauigkeit der Berechnung.

**Parameterübergabe:**
Die neue Funktion nimmt den radius als Parameter entgegen, anstatt ihn aus request.form zu extrahieren. Dies macht die Funktion unabhängiger von der Flask-Umgebung und somit flexibler einsetzbar.

**Entfernung der Typumwandlung:**
Die explizite Umwandlung zu float() wurde entfernt. Dies verlagert die Verantwortung für die korrekte Typübergabe auf den Aufrufer der Funktion.

**Hinzufügen eines Docstrings:**
Die neue Funktion enthält einen Docstring, der ihre Funktionalität beschreibt. Dies verbessert die Lesbarkeit und Dokumentation des Codes.

**Entfernung des try-Blocks:**


Der try-Block wurde entfernt. Die Fehlerbehandlung wird nun außerhalb dieser Funktion durchgeführt, was eine klarere Trennung von Berechnung und Fehlerbehandlung ermöglicht.


### 5. Debug-Modus deaktiviert

- **Änderung**: Der Debug-Modus ist auf `False` gesetzt.
- **Erklärung**: In einer Produktionsumgebung sollte der Debug-Modus deaktiviert sein, um potenzielle Sicherheitslücken zu vermeiden und keine sensiblen Informationen preiszugeben.
- 
**Code bevor**
```python
app.run(host='0.0.0.0', port=5005, debug=True)
```

**Code danach**
```python
app.run(host='0.0.0.0', port=5005, debug=True)
```


## Fazit

Durch die Kombination dieser Ansätze entsteht ein Code, der sowohl sicher und robust als auch kompakt und effizient ist – ideal für den Einsatz in einer Produktionsumgebung.

Diese Änderungen verbessern die Wartbarkeit, Fehlerdiagnose und Cloud-Bereitschaft der Anwendung erheblich. Logging und robuste Fehlerbehandlung sind wesentliche Bestandteile einer Produktionsumgebung, und die Unterstützung für AWS Lambda bietet eine skalierbare Bereitstellungsoption. Der Wechsel des Datenbankpfads zu `/tmp` und die Anpassungen im Ausführungsablauf tragen dazu bei, dass die Anwendung in verschiedenen Umgebungen konsistent und zuverlässig läuft.
