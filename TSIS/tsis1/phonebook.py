import psycopg2
import csv
import json 
import os
from connect import conn


# ---------- CREATE TABLES ----------

def load_schema():
    base_dir = os.path.dirname(__file__)

    with open(os.path.join(base_dir, "schema.sql"), "r") as f:
        sql = f.read()

    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()

    print("Schema loaded\n")
    print("Tables created successfully\n")


# ---------- INSERT ----------

def insert_contact(name, email, birthday, group_id, phones):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        for phone, p_type in phones:
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, p_type))

        conn.commit()


def insert_from_console():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_id = int(input("Group ID: "))

    phones = []
    count = int(input("How many phones: "))

    for _ in range(count):
        phone = input("Phone: ")
        p_type = input("Type (home/work/mobile): ")
        phones.append((phone, p_type))

    insert_contact(name, email, birthday, group_id, phones)
    print("Added successfully\n")


# ---------- CSV ----------
def insert_from_csv():
    with conn.cursor() as cur:
        with open("contacts.csv", "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # sanitize input
                name = row["name"].strip()
                email = row["email"].strip() if row["email"] else None
                birthday = row["birthday"].strip() if row["birthday"] else None
                group_name = row["group"].strip()

                # get or create group
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                group = cur.fetchone()

                if group:
                    group_id = group[0]
                else:
                    cur.execute(
                        "INSERT INTO groups (name) VALUES (%s) RETURNING id",
                        (group_name,)
                    )
                    group_id = cur.fetchone()[0]

                # insert contact
                cur.execute("""
                    INSERT INTO contacts (name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

                # insert phones
                phones = row["phones"].split(";")

                for p in phones:
                    if "-" not in p:
                        continue

                    number, p_type = p.split("-", 1)

                    number = number.strip()
                    p_type = p_type.strip().lower()

                    if p_type not in ("home", "work", "mobile"):
                        continue

                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, number, p_type))

        conn.commit()

    print("CSV imported successfully")


# ---------- SELECT ----------

def get_all_contacts(choice):
    allowed_columns = {
        "id": "c.id",
        "birthday": "c.birthday",
        "email": "c.email"
    }

    if choice in allowed_columns:
        print(choice)

    if choice not in allowed_columns:
        print("Invalid choice")
        return []

    with conn.cursor() as cur:
        query = f"""
            SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY {allowed_columns[choice]}
        """
        cur.execute(query)
        return cur.fetchall()
    

def show_full():
    with conn.cursor() as cur:
        cur.execute("SELECT current_database();")
        print("Connected to:", cur.fetchone())

        cur.execute("SELECT * FROM contacts;")
        rows = cur.fetchall()

        print("Rows count:", len(rows))

        for row in rows:
            print(row)

def print_contacts(contacts):
    if not contacts:
        print("(no contacts)")
        return

    for c in contacts:
        print(f"[{c[0]}] {c[1]} | {c[2]} | {c[3]} | {c[4]} | {c[5]} ({c[6]})")


# ---------- UPDATE ----------

def update():
    contact_id = int(input("Contact ID: "))
    field = input("What to update (name/email/birthday): ")
    new_value = input("New value: ")

    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE contacts SET {field} = %s WHERE id = %s",
            (new_value, contact_id)
        )
        conn.commit()

    print("Updated\n")

# ---------- FIND ----------

def find_by_pattern():
    print("Search by:")
    print("1. Name")
    print("2. Phone")
    print("3. Email")
    print("4. Group")

    choice = input("Choose option: ")
    pattern = input("Enter pattern: ").strip()

    with conn.cursor() as cur:
        if choice == "1":
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE c.name ILIKE %s
                ORDER BY c.id
            """, (f"%{pattern}%",))

        elif choice == "2":
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE p.phone ILIKE %s
                ORDER BY c.id
            """, (f"%{pattern}%",))

        elif choice == "3":
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE c.email ILIKE %s
                ORDER BY c.id
            """, (f"%{pattern}%",))

        elif choice == "4":
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE g.name ILIKE %s
                ORDER BY c.id
            """, (f"%{pattern}%",))

        else:
            print("Invalid choice")
            return []

        return cur.fetchall()

# ---------- DROP TABLE ----------

def drop_table():
    command = """DROP TABLE IF EXISTS phones CASCADE;
                 DROP TABLE IF EXISTS contacts CASCADE;
                 DROP TABLE IF EXISTS groups CASCADE;"""

    with conn.cursor() as cur:
        cur.execute(command)
        conn.commit()

# ---------- FILTER BY GROUP ----------

def filter_by_group():
    group = input("Enter group name: ").strip()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name ILIKE %s
            ORDER BY c.id
        """, (f"%{group}%",))

        return cur.fetchall()

# ---------- PAGINATION ----------

def pagination():
    page = 0
    size = 5

    while True:
        offset = page * size

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM pagination(%s, %s);",
                (size, offset)
            )
            rows = cur.fetchall()

        if not rows:
            print("No more data")
            if page > 0:
                page -= 1
            continue

        print(f"\nPage: {page + 1}")
        print_contacts(rows)

        cmd = input("n-next | p-prev | q-quit: ").lower()

        if cmd == "n":
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1
        elif cmd == "q":
            break
# ---------- PROCEDURES ----------

def insert_by_name():
    name = input("Name: ")
    phone = input("Phone: ")

    with conn.cursor() as cur:
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()

    print("Upsert done\n")


def insert_many_names():
    names = input("Names: ").split()
    phones = input("Phones: ").split()

    if len(names) != len(phones):
        print("Mismatch!")
        return

    with conn.cursor() as cur:
        cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
        conn.commit()

    print("Inserted many\n")


def delete_proc():
    print("Delete contact by:")
    print("- ID (e.g. 5)")
    print("- Name (e.g. Sergey)")
    print("- Email (e.g. test@mail.com)")
    print("- Birthday (YYYY-MM-DD)")
    print("- Phone (e.g. exact phone number)")

    value = input("Enter value: ").strip()

    with conn.cursor() as cur:
        # count contacts before delete
        cur.execute("SELECT COUNT(*) FROM contacts")
        before = cur.fetchone()[0]

        # call procedure
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()

        # count after delete
        cur.execute("SELECT COUNT(*) FROM contacts")
        after = cur.fetchone()[0]

    deleted = before - after

    if deleted > 0:
        print(f"Deleted {deleted} contact(s)\n")
    else:
        print("No contacts were deleted\n")

def add_phone_console():
    contact_id = input("Enter contact ID: ").strip()

    if not contact_id.isdigit():
        print("Invalid ID\n")
        return

    phone = input("Enter phone: ").strip()
    p_type = input("Type (home/work/mobile): ").strip().lower()

    with conn.cursor() as cur:
        cur.execute(
            "CALL add_phone(%s, %s, %s)",
            (int(contact_id), phone, p_type)
        )
        conn.commit()

    print("Phone added\n")

def move_to_group_console():
    contact_id = input("Enter contact ID: ").strip()

    if not contact_id.isdigit():
        print("Invalid ID\n")
        return

    group = input("Enter new group name: ").strip()

    with conn.cursor() as cur:
        cur.execute(
            "CALL move_to_group(%s, %s)",
            (int(contact_id), group)
        )
        conn.commit()

    print("Group updated\n")

# ---------- LOAD SQL ----------

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "functions.sql"), "r") as f:
    with conn.cursor() as cur:
        cur.execute(f.read())
    conn.commit()

with open(os.path.join(base_dir, "procedures.sql"), "r") as d:
    with conn.cursor() as cur:
        cur.execute(d.read())
    conn.commit()

#---------- EXPORT TO JSON ----------

def export_to_json():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                c.id, c.name, c.email, c.birthday, g.name,
                p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id
        """)

        rows = cur.fetchall()

    data = {}

    for r in rows:
        cid = r[0]

        if cid not in data:
            data[cid] = {
                "name": r[1],
                "email": r[2],
                "birthday": str(r[3]) if r[3] else None,
                "group": r[4],
                "phones": []
            }

        if r[5]:
            data[cid]["phones"].append({
                "number": r[5],
                "type": r[6]
            })

    result = list(data.values())

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("Exported to contacts.json")

#---------- IMPORT FROM JSON ----------

def import_from_json():
    import json

    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with conn.cursor() as cur:
        for contact in data:
            name = contact["name"]
            email = contact["email"]
            birthday = contact["birthday"]
            group_name = contact["group"]

            # check duplicate
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing = cur.fetchone()

            if existing:
                action = input(f"{name} exists. skip / overwrite: ").lower()

                if action == "skip":
                    continue

                elif action == "overwrite":
                    cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))

                else:
                    continue

            # group
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group = cur.fetchone()

            if group:
                group_id = group[0]
            else:
                cur.execute(
                    "INSERT INTO groups (name) VALUES (%s) RETURNING id",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]

            # insert contact
            cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            # phones
            for p in contact["phones"]:
                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, p["number"], p["type"]))

        conn.commit()

    print("Imported from JSON")

# ---------- MENU ----------

while True:
    command = int(input("""
1. Create tables
2. Insert from console
3. Insert from csv
4. Update
5. Show contacts
6. Find by pattern
7. Pagination
8. Delete by name|id|phone|birthday|email
9. Add phone
10. Filter by group
11. Export to json
12. Import from json 
13. Move to group
0. Exit

Choose: """))

    if command == 1:
        load_schema()

    elif command == 2:
        insert_from_console()

    elif command == 3:
        insert_from_csv()

    elif command == 4:
        update()

    elif command == 5:
        choice = input("Order by (id/birthday/email): ")
        # print(choice)
        print_contacts(get_all_contacts(choice))

    elif command == 6:
        print_contacts(find_by_pattern())

    elif command == 7:
        pagination()

    elif command == 8:
        delete_proc()

    elif command == 9:
        add_phone_console()

    elif command == 10:
        print_contacts(filter_by_group())
    
    elif command == 11:
        export_to_json()
    
    elif command == 12:
        import_from_json()
    
    elif command == 13:
        move_to_group_console()

    elif command == 14:
        show_full()
    

    elif command == 99:
        drop_table()

    elif command == 0:
        break


conn.close()
print("Goodbye!")