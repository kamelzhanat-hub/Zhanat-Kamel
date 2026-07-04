import psycopg2
from connect import get_connection

def search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()
    
    print("\n--- Search Results ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    if not rows:
        print("No contacts found.")
    
    cur.close()
    conn.close()


def paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    
    print(f"\n--- Page (Limit: {limit}, Offset: {offset}) ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    if not rows:
        print("No records on this page.")
        
    cur.close()
    conn.close()


def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()
    
    print(f"Contact '{name}' successfully processed (inserted/updated).")
    cur.close()
    conn.close()


def bulk_insert(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    
   
    names = [n.strip() for n in names if n.strip()]
    phones = [p.strip() for p in phones if p.strip()]
    
    
    cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
    conn.commit()
    
    
    if conn.notices:
        print("\nDatabase Validation Notices:")
        for notice in conn.notices:
            print(notice.strip())
            
    print("Bulk insert operation completed.")
    cur.close()
    conn.close()


def delete(value):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("CALL delete_contact(%s);", (value,))
    conn.commit()
    
    print(f"Delete operation for '{value}' completed.")
    cur.close()
    conn.close()


if __name__ == "__main__":
    while True:
        print("\n=== PhoneBook Menu (Practice 8) ===")
        print("1 - Search")
        print("2 - Paginate")
        print("3 - Upsert")
        print("4 - Bulk Insert")
        print("5 - Delete")
        print("6 - Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            search(input("Enter pattern: "))
        elif choice == "2":
            try:
                limit = int(input("Limit: "))
                offset = int(input("Offset: "))
                paginate(limit, offset)
            except ValueError:
                print("Please enter valid integers.")
        elif choice == "3":
            upsert(input("Name: "), input("Phone: "))
        elif choice == "4":
            names_input = input("Names (comma separated): ").split(",")
            phones_input = input("Phones (comma separated): ").split(",")
            if len(names_input) == len(phones_input):
                bulk_insert(names_input, phones_input)
            else:
                print("Error: Number of names and phones must match!")
        elif choice == "5":
            delete(input("Enter name or phone: "))
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")