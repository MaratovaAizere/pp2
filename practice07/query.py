from db_connect import get_connection

def query_data():
    keyword = input("Search (name or phone): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s OR phone ILIKE %s",
        (f"%{keyword}%", f"%{keyword}%")
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    query_data()