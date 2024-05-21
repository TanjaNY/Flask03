from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
import os

app = Flask(__name__)

# Konfiguration der Datenbankverbindung
BASE_DIR = os.getcwd()
db_path = os.path.join(BASE_DIR, "circle_calculations.db")


def get_db_connection():
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.
    Rückgabe:
        Ein sqlite3.Connection-Objekt, das die Verbindung zur Datenbank darstellt.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Ermöglicht den Zugriff auf Daten nach Spaltennamen
    return conn

def create_table():
    """
    Erstellt die Tabelle 'calculations' in der SQLite-Datenbank, wenn sie noch nicht vorhanden ist.
    """
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        radius REAL NOT NULL,
        area REAL NOT NULL,
        timestamp DATETIME NOT NULL
    )''')
    conn.commit()
    conn.close()




@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM calculations ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()
    return render_template('index.html', results=results)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        radius = float(request.form['radius'])
        area = round(3.14159 * radius ** 2, 2)

        # Speichert das Berechnungsergebnis und den Zeitstempel in der Datenbank
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO calculations (radius, area, timestamp) VALUES (?, ?, ?)',
                       (radius, area, datetime.datetime.now()))
        conn.commit()
        conn.close()

        return render_template('index.html', radius=radius, result=area, success=True)
    except ValueError:
        return render_template('index.html', result=None, error="Ungültige Eingabe")


@app.route('/delete/<int:calculation_id>', methods=['GET', 'POST'])
def delete(calculation_id):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM calculations WHERE id = ?', (calculation_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        # Anzeige der Bestätigungsseite vor der Löschung (optional)
        return render_template('delete.html', calculation_id=calculation_id)


if __name__ == '__main__':
    # Stellt eine Verbindung zur Datenbank her
    conn = get_db_connection()

    # Erstellt die Tabelle nur, wenn sie nicht vorhanden ist
    create_table()

    # Schließt die Verbindung nach dem Erstellen der Tabelle
    conn.close()

    # Startet die Flask-Anwendung
   
    app.run(host='0.0.0.0', port=5005, debug=True)
