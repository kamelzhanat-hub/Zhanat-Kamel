import psycopg2
from config import DB_PARAMS

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(20) UNIQUE NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Table checked/created successfully.")