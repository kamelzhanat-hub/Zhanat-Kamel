-- 1. функция поиска по паттерну
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.first_name, c.phone_number 
    FROM phonebook c
    WHERE c.first_name ILIKE '%' || p_pattern || '%' 
       OR c.phone_number LIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 4. пагинация
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.first_name, c.phone_number 
    FROM phonebook c
    ORDER BY c.id
    LIMIT p_limit 
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;