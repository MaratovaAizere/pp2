import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="24680",
        host="localhost",
        port="5432"
    )