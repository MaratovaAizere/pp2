from connect import get_connection


def search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()


def paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()


def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()
    
    conn.close()


def bulk_insert(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
    conn.commit()
    
    conn.close()


def delete(value):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("CALL delete_contact(%s);", (value,))
    conn.commit()
    
    conn.close()


if __name__ == "__main__":
    print("1 - Search")
    print("2 - Paginate")
    print("3 - Upsert")
    print("4 - Bulk Insert")
    print("5 - Delete")

    choice = input("Choose: ")

    if choice == "1":
        search(input("Enter pattern: "))
    elif choice == "2":
        paginate(int(input("Limit: ")), int(input("Offset: ")))
    elif choice == "3":
        upsert(input("Name: "), input("Phone: "))
    elif choice == "4":
        names = input("Names (comma): ").split(",")
        phones = input("Phones (comma): ").split(",")
        bulk_insert(names, phones)
    elif choice == "5":
        delete(input("Enter name or phone: "))