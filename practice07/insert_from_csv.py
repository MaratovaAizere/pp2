import csv
from db_connect import get_connection

def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    insert_from_csv("data.csv")