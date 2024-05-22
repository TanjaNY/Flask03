
# Eine Flask-Anwendung erstellen

# Flask02
Das ist die zweite Flask-Lektion, die erste Lektion findest du hier:https://github.com/TanjaNY/Flask


## 1. Hinzufügen einer Datenbank zur Anwendung
Wir haben eine Web-Anwendung erstellt. Jetzt möchten wir alle Ergebnisse speichern. Dafür benötigen wir eine Datenbank. Wir werden SQLite verwenden.

## Was ist SQLite?
SQLite ist ein leichtgewichtiges, serverloses Datenbankmanagementsystem, das auf einer einzigen Datei basiert. Es bietet eine vollständige SQL-Unterstützung und ist eine einfache Lösung für die Speicherung und Verwaltung von Daten in Anwendungen.

## Warum ist SQLite für eine kleine und leichte Flask-Anwendung geeignet?
Es gibt mehrere Gründe, warum SQLite für eine kleine und leichte Flask-Anwendung geeignet ist:

- **Einfache Integration:** SQLite kann problemlos in Python-Anwendungen wie Flask integriert werden. Es gibt verschiedene Python-Bibliotheken, die die Interaktion mit SQLite-Datenbanken vereinfachen, wie zum Beispiel sqlite3 oder SQLAlchemy.
- **Kein zusätzlicher Server erforderlich:** Da SQLite serverlos ist, benötigen Sie keinen zusätzlichen Datenbankserver, der separat installiert und verwaltet werden muss. Dies reduziert die Komplexität und vereinfacht den Prozess der Anwendungsentwicklung.
- **Niedrige Ressourcennutzung:** SQLite hat geringe Anforderungen an Speicher, Rechenleistung und andere Systemressourcen. Dies macht es ideal für Anwendungen mit begrenzten Ressourcen oder für Prototypen und kleine Anwendungen.
- **Portabilität:** SQLite-Datenbanken sind in einer einzigen Datei gespeichert, was sie leicht zu verschieben und zu verwalten macht. Dadurch können Sie die Datenbank problemlos zwischen verschiedenen Systemen und Entwicklungsumgebungen verschieben.

Im Allgemeinen bietet SQLite eine einfache, effiziente und kostengünstige Möglichkeit zum Speichern und Verwalten von Daten in kleinen und leichten Flask-Anwendungen.
In unserer Anwendung haben wir uns für die Verwendung von SQLite entschieden und benötigen daher keinen Datenbankcontainer. Allerdings müsste bei der Verwendung anderer Datenbanken wie MySQL oder PostgreSQL ein Datenbankcontainer eingerichtet werden. In diesem Fall müsste die Datei docker-compose.yaml bzw. compose.yaml angepasst werden, um den Datenbankcontainer hinzuzufügen.

## 2. Integration von SQLite
Vorbereitungen:

Stellen Sie sicher, dass Sie die sqlite3-Bibliothek installiert haben:

```bash
pip install sqlite3
```

Aktualisieren der Datei app.py:

Die Datei app.py enthält den Hauptcode unserer Anwendung. Wir aktualisieren sie nun für die SQLite-Integration.

### Änderungen in app.py:

Importieren der Bibliothek:

Python

```bash
import sqlite3
```
Verbinden zur Datenbank:

Python
```bash
conn = sqlite3.connect('flask_app.db')
c = conn.cursor()
```
Tabelle calculations erstellen:

Python
```bash
c.execute('''CREATE TABLE IF NOT EXISTS calculations (
                radius REAL,
                area REAL
            )''')
```
Speichern von Berechnungsergebnissen:

Python
```bash
def save_calculation(radius, area):
    c.execute('INSERT INTO calculations (radius, area) VALUES (?, ?)', (radius, area))
    conn.commit()
```
Abrufen gespeicherter Ergebnisse:

Python
```bash
def get_calculations():
    c.execute('SELECT * FROM calculations')
    return c.fetchall()
```

Löschen von Berechnungseinträgen:

Python
```bash
def delete_calculation(calculation_id):
    c.execute('DELETE FROM calculations WHERE id = ?', (calculation_id,))
    conn.commit()
```
### Anpassen der Routen:

Aktualisieren Sie die Routen "/" und "/calculate" für die neuen Funktionen.
Aktualisieren der Datei templates/index.html:

Die Datei index.html enthält die HTML-Vorlage. Wir aktualisieren sie, um die gespeicherten Ergebnisse anzuzeigen und das Löschen einzelner Einträge zu ermöglichen.

### Änderungen in index.html:

Im Abschnitt zum Anzeigen gespeicherter Berechnungen werden HTML, Jinja2-Template-Syntax und Bootstrap-CSS-Klassen verwendet. Die HTML-Struktur wird verwendet, um eine Tabelle mit den Spalten "Radius", "Fläche" und "Aktion" zu definieren. Die Bootstrap-Klasse table wird verwendet, um die Tabelle stilvoll und für mobile Geräte ansprechend zu gestalten.
Jinja2-Syntax wird verwendet, um die Daten aus der Datenbank zu rendern und dynamische Inhalte innerhalb der HTML-Seite zu erstellen. Das {% for %}-Schleifenelement iteriert über alle berechneten Werte in der Variablen calculations und fügt eine neue Zeile für jeden berechneten Radius und die zugehörige Fläche hinzu. Zudem gibt es einen Link zum Löschen der berechneten Werte aus der Datenbank.
Die Kombination von HTML, CSS, JavaScript und Template-Engines wie Jinja2 ermöglicht es, komplexe und benutzerfreundliche Webapplikationen zu erstellen, indem sie Präsentation, Interaktion und Inhaltsgenerierung effizient und effektiv kombinieren.

HTML
```bash
{% if calculations %}
    <h2>Gespeicherte Berechnungen</h2>
    <table class="table">
        <thead>
            <tr>
                <th>Radius</th>
                <th>Fläche</th>
                <th>Aktion</th>
            </tr>
        </thead>
        <tbody>
            {% for calculation in calculations %}
                <tr>
                    <td>{{ calculation.radius }}</td>
                    <td>{{ calculation.area }}</td>
                    <td>
                        <a href="/delete/{{ calculation.id }}">Löschen</a>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endif %}
```


## 2. app.py erwetern
Am besten öffnen wir beide Dateien app.py (Flask01) und app.py(Flask02) und vergleichen die beide.
Die zwei Versionen der Flask-Anwendung unterscheiden sich im Wesentlichen durch die Integration einer SQLite-Datenbank in der zweiten Version. Hier sind die wichtigsten Unterschiede:
## Erste Version
### Einfache Flask-Anwendung mit zwei Routen:

'/' zum Rendern der Index-Seite

'/calculate' zur Verarbeitung einer POST-Anfrage mit dem Radius und dem Rendern der Ergebnisse auf der Index-Seite.

Kein Speichern von Daten in einer Datenbank.

## Zweite Version
### Integration einer SQLite-Datenbank zum Speichern von Daten.

Mehrere Funktionen zur Verbindungsherstellung mit der Datenbank und Tabelle calculations.
Mehrere neue Routen:

'/' zum Rendern der Index-Seite mit allen gespeicherten Berechnungsergebnissen aus der Datenbank.
        
'/calculate' zur Verarbeitung einer POST-Anfrage, Speichern des Berechnungsergebnisses in der Datenbank und Rendern der Ergebnisse auf der Index-Seite.

'/ delete/<int:calculation_id>' zum Löschen eines bestimmten Eintrags aus der Datenbank.

Im Allgemeinen bietet die zweite Version eine bessere Datenverwaltung durch die Integration einer SQLite-Datenbank. Diese ermöglicht das Speichern, Abfragen und Löschen von Berechnungsergebnissen, was die Funktionalität der Anwendung erweitert und sie für komplexere Anwendungsfälle geeignet macht.

## 3. Die Anwendung starten.

- Navigiere zum Verzeichnis der geklonten Flask-Anwendung.
- Aktiviere die Conda-Umgebung mit dem Befehl:

```bash
flask_env\Scripts\activate
```
- Stare  die Flask-Anwendung
```bash
flask run
```

Wir öffnen unser Webbrowser und geben die Adresse [http://127.0.0.1:5000](http://127.0.0.1:5000) in die Adressleiste ein, um unsere Anwendung zu sehen.

<p>&nbsp;</p>

<p><img src="https://github.com/TanjaNY/Flask/blob/main/pics/Flask02.png" alt="Flask App" &nbsp;&nbsp;&nbsp;&nbsp /></p>

<p>&nbsp;</p>

### Wir können beobachten wie veränderte sich unsere Anwendung.

<p>&nbsp;</p>

<p><img src="https://github.com/TanjaNY/Flask/blob/main/pics/flask01.png" widht="100" height="200" alt="Flask App" &nbsp;&nbsp;&nbsp;&nbsp /></p>
<p>&nbsp;</p>
<p>&nbsp;</p>



<p><img src="https://github.com/TanjaNY/Flask/blob/main/pics/Flask003.png" widht="300" height="500" alt="Flask App" &nbsp;&nbsp;&nbsp;&nbsp /></p>


<p>&nbsp;</p>

### Du kannst noch mal mit dem Containesieren probieren.


