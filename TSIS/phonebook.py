import csv
import json
import os
from connect import get_connection


# 1 Инициализация базы / Database Init

def init_db():
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return
    try:
        with conn:
            with conn.cursor() as cur:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                schema_path = os.path.join(base_dir, 'schema.sql')
                if os.path.exists(schema_path):
                    with open(schema_path, 'r', encoding='utf-8') as f:
                        cur.execute(f.read())
                cur.execute("""
                    DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);
                    DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);
                    
                    CREATE OR REPLACE PROCEDURE add_phone(
                        p_contact_name VARCHAR, 
                        p_phone VARCHAR, 
                        p_type VARCHAR
                    )
                    AS $$
                    DECLARE
                        v_contact_id INTEGER;
                    BEGIN
                        SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
                        IF v_contact_id IS NULL THEN
                            RAISE EXCEPTION 'Contact % not found', p_contact_name;
                        END IF;
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (v_contact_id, p_phone, p_type);
                    END;
                    $$ LANGUAGE plpgsql;

                    CREATE OR REPLACE PROCEDURE move_to_group(
                        p_contact_name VARCHAR, 
                        p_group_name VARCHAR
                    )
                    AS $$
                    DECLARE
                        v_group_id INTEGER;
                        v_contact_id INTEGER;
                    BEGIN
                        SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
                        IF v_group_id IS NULL THEN
                            INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
                        END IF;

                        SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
                        IF v_contact_id IS NULL THEN
                            INSERT INTO contacts (name, group_id) VALUES (p_contact_name, v_group_id);
                        ELSE
                            UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
                        END IF;
                    END;
                    $$ LANGUAGE plpgsql;
                """)
                
                cur.execute("""
                    CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
                    RETURNS TABLE(
                        contact_id INTEGER,
                        contact_name VARCHAR,
                        email VARCHAR,
                        birthday DATE,
                        phone_number VARCHAR,
                        phone_type VARCHAR
                    ) AS $$
                    BEGIN
                        RETURN QUERY
                        SELECT c.id, c.name, c.email, c.birthday, p.phone, p.type
                        FROM contacts c
                        LEFT JOIN groups g ON c.group_id = g.id
                        LEFT JOIN phones p ON c.id = p.contact_id
                        WHERE c.name ILIKE '%' || p_query || '%'
                           OR c.email ILIKE '%' || p_query || '%'
                           OR p.phone ILIKE '%' || p_query || '%';
                    END;
                    $$ LANGUAGE plpgsql;
                """)
        print("Database initialized, procedures registered successfully.")
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()


# 2 Extended CSV Import

def import_from_csv(filename='contacts.csv'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)

    if not os.path.exists(full_path):
        print(f"File {filename} not found.")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                with open(full_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cur.execute("CALL move_to_group(%s::varchar, %s::varchar);", (row['name'], row['group']))
                        
                        email = row['email'].strip() if row['email'].strip() else None
                        birthday = row['birthday'].strip() if row['birthday'].strip() else None
                        
                        cur.execute("""
                            UPDATE contacts 
                            SET email = %s, birthday = %s 
                            WHERE name = %s;
                        """, (email, birthday, row['name']))
                        
                        cur.execute("CALL add_phone(%s::varchar, %s::varchar, %s::varchar);", (row['name'], row['phone'], row['phone_type']))
        print(f"Data successfully imported from {filename}.")
    except Exception as e:
        print(f"Error during CSV import: {e}")
    finally:
        conn.close()

# 3 JSON Export / Import

def export_to_json(filename='contacts.json'):
    conn = get_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.name, c.email, c.birthday, g.name as group_name, 
                           json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    GROUP BY c.id, g.name;
                """)
                rows = cur.fetchall()
                
                data = []
                for row in rows:
                    data.append({
                        "name": row[0],
                        "email": row[1],
                        "birthday": str(row[2]) if row[2] else None,
                        "group": row[3],
                        "phones": row[4] if row[4] and row[4][0]['phone'] else []
                    })
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported to {filename}.")
    except Exception as e:
        print(f"Export error: {e}")
    finally:
        conn.close()

def import_from_json(filename='contacts.json'):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    conn = get_connection()
    if not conn:
        return

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        for item in data:
            name = item['name']
            
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
                    exists = cur.fetchone()
            
            if exists:
                choice = input(f"Contact '{name}' already exists. Skip or Overwrite? (s/o): ").lower()
                if choice == 's':
                    continue
                elif choice == 'o':
                    with conn:
                        with conn.cursor() as cur:
                            cur.execute("DELETE FROM contacts WHERE name = %s;", (name,))
            
            with conn:
                with conn.cursor() as cur:
                    cur.execute("CALL move_to_group(%s::varchar, %s::varchar);", (name, item['group']))
                    cur.execute("""
                        UPDATE contacts SET email = %s, birthday = %s WHERE name = %s;
                    """, (item['email'], item['birthday'], name))
                    
                    for p in item['phones']:
                        cur.execute("CALL add_phone(%s::varchar, %s::varchar, %s::varchar);", (name, p['phone'], p['type']))
        print("JSON Import completed.")
    except Exception as e:
        print(f"JSON Import error: {e}")
    finally:
        conn.close()


# 4 Search & Pagination

def view_contacts_paginated():
    query = input("Enter search query (name/email/phone, leave empty for all): ")
    group_filter = input("Enter group to filter by (or leave empty for all): ").strip()
    
    print("\nSort options: [1] Name, [2] Birthday, [3] Contact ID (Date created)")
    sort_choice = input("Select sort option (default is Name): ").strip()
    
    if sort_choice == '2':
        sort_column = "birthday"
    elif sort_choice == '3':
        sort_column = "contact_id"
    else:
        sort_column = "contact_name"

    page = 0
    limit = 2
    
    while True:
        offset = page * limit
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    sql = f"""
                        SELECT contact_name, email, birthday, phone_number, phone_type 
                        FROM search_contacts(%s)
                        WHERE (%s = '' OR contact_id IN (
                            SELECT id FROM contacts WHERE group_id = (SELECT id FROM groups WHERE name ILIKE %s)
                        ))
                        ORDER BY {sort_column} NULLS LAST
                        LIMIT %s OFFSET %s;
                    """
                    cur.execute(sql, (query, group_filter, group_filter, limit, offset))
                    rows = cur.fetchall()
                    
                    if not rows and page > 0:
                        print("\n--- No more contacts on this page. ---")
                        page -= 1
                        continue
                    
                    print(f"\n--- Page {page + 1} (Sorted by {sort_column}) ---")
                    if not rows:
                        print("No contacts found.")
                    for row in rows:
                        print(f"Name: {row[0]} | Email: {row[1]} | Bday: {row[2]} | Phone: {row[3]} ({row[4]})")
        except Exception as e:
            print(f"Error fetching data: {e}")
            break
        finally:
            conn.close()
            
        action = input("\nType [n]ext page, [p]rev page, or [q]uit: ").lower()
        if action == 'n':
            page += 1
        elif action == 'p':
            if page > 0:
                page -= 1
            else:
                print("You are on the first page.")
        elif action == 'q':
            break


# 5 Main Menu Loop

def main():
    init_db()  
    while True:
        print("\n=== Extended PhoneBook Menu ===")
        print("1. Import from CSV")
        print("2. Export to JSON")
        print("3. Import from JSON")
        print("4. Search & View Contacts (with Pagination)")
        print("5. Exit")
        
        choice = input("Select an option: ")
        if choice == '1':
            import_from_csv()
        elif choice == '2':
            export_to_json()
        elif choice == '3':
            import_from_json()
        elif choice == '4':
            view_contacts_paginated()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()