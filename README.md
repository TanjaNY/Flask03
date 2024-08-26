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


### 1. Datenbankinitialisierung mit dem Kontextmanager für Datenbankoperationen (`with`-Statements)


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

### 2. Fehlerbehandlung und Logging

- **Änderung**: Fehlerbehandlungsmechanismen (`try-except`) wurden in den Funktionen `get_db_connection()`, `init_db()`, `index()`, `calculate()` und `delete()` beibehalten, ergänzt durch das Logging mit `app.logger.error()`.
- **Erklärung**: Die Fehlerbehandlung sorgt dafür, dass die Anwendung stabil bleibt, auch wenn unerwartete Fehler auftreten. Das Logging ermöglicht es, Fehler detailliert zu protokollieren, was besonders für die Fehlerbehebung in der Produktion wichtig ist.

### 2. Nutzung von `math.pi`

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
### 5. Debug-Modus deaktiviert

- **Änderung**: Der Debug-Modus ist auf `False` gesetzt.
- **Erklärung**: In einer Produktionsumgebung sollte der Debug-Modus deaktiviert sein, um potenzielle Sicherheitslücken zu vermeiden und keine sensiblen Informationen preiszugeben.

## Fazit

Durch die Kombination dieser Ansätze entsteht ein Code, der sowohl sicher und robust als auch kompakt und effizient ist – ideal für den Einsatz in einer Produktionsumgebung.

Diese Änderungen verbessern die Wartbarkeit, Fehlerdiagnose und Cloud-Bereitschaft der Anwendung erheblich. Logging und robuste Fehlerbehandlung sind wesentliche Bestandteile einer Produktionsumgebung, und die Unterstützung für AWS Lambda bietet eine skalierbare Bereitstellungsoption. Der Wechsel des Datenbankpfads zu `/tmp` und die Anpassungen im Ausführungsablauf tragen dazu bei, dass die Anwendung in verschiedenen Umgebungen konsistent und zuverlässig läuft.
