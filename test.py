import sqlite3
import unittest
from app import get_db_connection, create_table

class TestCreateTable(unittest.TestCase):
    def setUp(self):
        self.conn = get_db_connection()  # Establish a connection to the test database
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.execute("DROP TABLE IF EXISTS calculations")  # Clean up the test database
        self.conn.close()

    def test_table_creation(self):
        create_table(self.conn)  # Create the table
        # Check if the table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='calculations'")
        table_exists = self.cursor.fetchone()
        self.assertIsNotNone(table_exists, "Table 'calculations' does not exist")

    def test_table_structure(self):
        create_table(self.conn)  # Create the table
    # Get the table schema
        self.cursor.execute("PRAGMA table_info(calculations)")
        table_info = self.cursor.fetchall()
    # Extract the relevant information from the fetched rows
        extracted_info = [(row[0], row[1], row[2], row[5]) for row in table_info]
    # Check if the extracted information matches the expected schema
        expected_schema = [
            (0, 'id', 'INTEGER', 1),
            (1, 'radius', 'REAL', 0),
            (2, 'area', 'REAL', 0),   
            (3, 'timestamp', 'DATETIME', 0)
        ]
        self.assertListEqual(extracted_info, expected_schema)

if __name__ == '__main__':
    unittest.main()
