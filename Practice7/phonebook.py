import csv
import psycopg2
from config import DB_PARAMS

# Import data from a CSV file
def import_from_csv(file_path):
    conn = None
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Подключаемся точно так же, как в твоем connect.py
            conn = psycopg2.connect(**DB_PARAMS)
            cur = conn.cursor()
            
            query = "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s) ON CONFLICT (phone_number) DO NOTHING;"
            data_to_insert = [(row['first_name'], row['phone_number']) for row in reader]
            
            cur.executemany(query, data_to_insert)
            conn.commit()
            cur.close()
            print("Data from CSV imported successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error during CSV import:", error)
    finally:
        if conn is not None:
            conn.close()

# Insert data entered from the console
def add_contact(name, phone):
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s);",
            (name, phone)
        )
        conn.commit()
        cur.close()
        print(f"Contact '{name}' added successfully.")
    except psycopg2.errors.UniqueViolation:
        print("Error: A contact with this phone number already exists!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error adding contact:", error)
    finally:
        if conn is not None:
            conn.close()

# Update a contact's first name or phone number
def update_contact(old_name, new_name=None, new_phone=None):
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        if new_name:
            cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s;", (new_name, old_name))
        if new_phone:
            cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s;", (new_phone, old_name))
            
        conn.commit()
        cur.close()
        print(f"Contact '{old_name}' updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error updating contact:", error)
    finally:
        if conn is not None:
            conn.close()

# Query contacts with different filters
def search_contacts(search_str):
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        query = "SELECT first_name, phone_number FROM phonebook WHERE first_name ILIKE %s OR phone_number LIKE %s;"
        cur.execute(query, (f"%{search_str}%", f"{search_str}%"))
        rows = cur.fetchall()
        
        print("\n--- Search Results ---")
        for row in rows:
            print(f"Name: {row[0]} | Phone: {row[1]}")
        if not rows:
            print("No contacts found.")
        print("----------------------")
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error searching contacts:", error)
    finally:
        if conn is not None:
            conn.close()

# Delete a contact by name or phone number
def delete_contact(search_param):
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s;", (search_param, search_param))
        conn.commit()
        cur.close()
        print(f"Contact(s) matching '{search_param}' deleted.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error deleting contact:", error)
    finally:
        if conn is not None:
            conn.close()

# Console User Interface
def main_menu():
    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Import contacts from CSV")
        print("2. Add contact manually")
        print("3. Update contact")
        print("4. Search contact (by name or phone prefix)")
        print("5. Delete contact")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            import_from_csv("Practice7/contacts.csv")
        elif choice == '2':
            name = input("Enter name: ").strip()
            phone = input("Enter phone number: ").strip()
            if name and phone: 
                add_contact(name, phone)
        elif choice == '3':
            old_name = input("Enter the name of the contact you want to update: ").strip()
            new_name = input("Enter new name (leave empty to skip): ").strip() or None
            new_phone = input("Enter new phone number (leave empty to skip): ").strip() or None
            if old_name: 
                update_contact(old_name, new_name, new_phone)
        elif choice == '4':
            search_str = input("Enter name or phone prefix to search: ").strip()
            search_contacts(search_str)
        elif choice == '5':
            param = input("Enter name or phone number to delete: ").strip()
            if param: 
                delete_contact(param)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()