import psycopg2
from config import DB_PARAMS

def create_tables():
    """Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) NOT NULL UNIQUE
        )
        """,
    )
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        for command in commands:
            cur.execute(command)
            
        cur.close()
        conn.commit()
        print("Database and table initialized successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error during DB initialization:", error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()