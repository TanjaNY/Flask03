from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
import os
from math import pi
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.exceptions import BadRequest, InternalServerError

app = Flask(__name__)

# Konfiguration der Datenbankverbindung
BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "circle_calculations.db")

# Logging-Konfiguration
file_handler = RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 10, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Logger-Konfiguration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def get_db_connection():
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.
    Rückgabe:
        Ein sqlite3.Connection-Objekt, das die Verbindung zur Datenbank darstellt.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Ermöglicht den Zugriff auf Daten nach Spaltennamen
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Database connection error: {e}")
        raise InternalServerError("Datenbankverbindungsfehler")


def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabelle 'calculations', wenn sie noch nicht vorhanden ist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                radius REAL NOT NULL,
                area REAL NOT NULL,
                timestamp DATETIME NOT NULL
            )''')
    except sqlite3.Error as e:
        app.logger.error(f"Database table creation error: {e}")
        raise InternalServerError("Fehler beim Erstellen der Datenbanktabelle")


def calculate_area(radius):
    """
    Berechnet die Fläche eines Kreises anhand des übergebenen Radius.
    """
    return round(pi * radius ** 2, 2)


@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            results = conn.execute('SELECT * FROM calculations ORDER BY timestamp DESC').fetchall()
        return render_template('index.html', results=results)
    except sqlite3.Error as e:
        app.logger.error(f"Database query error: {e}")
        return render_template('index.html', error="Fehler beim Abrufen der Daten")


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        radius = float(request.form['radius'])
        area = calculate_area(radius)

        with get_db_connection() as conn:
            conn.execute('INSERT INTO calculations (radius, area, timestamp) VALUES (?, ?, ?)',
                         (radius, area, datetime.datetime.now()))

        return render_template('index.html', radius=radius, result=area, success=True)
    except ValueError:
        return render_template('index.html', result=None, error="Ungültige Eingabe")
    except sqlite3.Error as e:
        app.logger.error(f"Database insertion error: {e}")
        return render_template('index.html', error="Fehler beim Speichern der Daten")


@app.route('/delete/<int:calculation_id>', methods=['POST'])
def delete(calculation_id):
    try:
        with get_db_connection() as conn:
            conn.execute('DELETE FROM calculations WHERE id = ?', (calculation_id,))
        return redirect(url_for('index'))
    except sqlite3.Error as e:
        app.logger.error(f"Database deletion error: {e}")
        return render_template('index.html', error="Fehler beim Löschen der Daten")


if __name__ == '__main__':
    # Initialisiert die Datenbank und stellt sicher, dass die Tabelle existiert
    init_db()

    # Startet die Flask-Anwendung
    app.run(host='0.0.0.0', port=5005, debug=False)
