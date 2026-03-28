from db_connect import get_connection

def check():
    try:
        conn = get_connection()
        print("Connection successful!")
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check()