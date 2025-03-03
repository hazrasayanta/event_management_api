import sqlite3

DB_FILE = "./events.db"

def reset_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        print("Cleaning database...")

        # Option 1: Delete all data but keep tables
        cursor.execute("DELETE FROM attendees;")
        cursor.execute("DELETE FROM events;")
        cursor.execute("DELETE FROM users;")

        # Option 2: Drop all tables
        # cursor.execute("DROP TABLE IF EXISTS attendees;")
        # cursor.execute("DROP TABLE IF EXISTS events;")
        # cursor.execute("DROP TABLE IF EXISTS users;")

        conn.commit()
        print("Database cleaned successfully!")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database()
