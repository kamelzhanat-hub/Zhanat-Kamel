-- 2. Upsert 
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook
        SET phone_number = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone_number)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- 3. Массовая вставка + валидация 
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF length(p_phones[i]) >= 10 AND length(p_phones[i]) <= 15 THEN
            
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_names[i]) THEN
                UPDATE phonebook SET phone_number = p_phones[i] WHERE first_name = p_names[i];
            ELSE
                INSERT INTO phonebook(first_name, phone_number) VALUES (p_names[i], p_phones[i]);
            END IF;
            
        ELSE
            RAISE NOTICE 'Incorrect data skipped: Name: %, Phone: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;


-- 5. Удаление
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR phone_number = p_value;
END;
$$;