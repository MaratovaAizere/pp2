from db_connect import get_connection

def update_contact():
    phone = input("Enter phone to update: ")
    new_name = input("New name (leave empty if not needed): ")
    new_phone = input("New phone (leave empty if not needed): ")

    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute("UPDATE phonebook SET name=%s WHERE phone=%s", (new_name, phone))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s", (new_phone, phone))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_contact()