import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    print("Connected to PostgreSQL")

except Exception as e:
    print("Connection error:", e)