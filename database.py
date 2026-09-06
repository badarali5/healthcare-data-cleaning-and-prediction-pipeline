import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

class DatabaseConnection:

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASS")
        self.pgdb_conn = None

    def connect(self):
        try:
            self.pgdb_conn = psycopg.connect(
                host=self.host,
                port=self.port,
                dbname=self.name,
                user=self.user,
                password=self.password
            )

            if self.pgdb_conn:
                print("DATABASE is connected.")
                return self.pgdb_conn

            else:
                print("Database connection failed.")

        except psycopg.Error as e:
            print(f"Except block running. Database connection failed: {e}")

    def disconnect(self):
        if self.pgdb_conn:
            self.pgdb_conn.close()
            print("Database connection closed.")


def get_db_connection():
    db = DatabaseConnection()
    conn = db.connect()

    try:
        yield conn
    finally:
        db.disconnect()