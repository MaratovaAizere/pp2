from db_connect import get_connection

def insert_manual():
    conn = get_connection()
    cur = conn.cursor()

    while True:
        name = input("Enter name (or 'exit' to stop): ")
        if name.lower() == "exit":
            break

        phone = input("Enter phone: ")

        cur.execute(
            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
            (name, phone)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    insert_manual()