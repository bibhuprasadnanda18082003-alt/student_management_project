
import sqlite3


# Database Connection
def get_connection():
    connection = sqlite3.connect("students.db")
    return connection


# Create Students Table
def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        marks INTEGER NOT NULL,
        course TEXT NOT NULL,
        image TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )
    """

    cursor.execute(query)

    connection.commit()
    connection.close()


# Execute Table Creation
create_table()
