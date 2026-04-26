CREATE OR REPLACE FUNCTION find_text_by_pattern(target_text text)
RETURNS SETOF contacts
AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM contacts
    WHERE contacts.name ILIKE '%' || target_text || '%'
       OR contacts.phone ILIKE '%' || target_text || '%';

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Name or phone with this pattern % not found', target_text;
    END IF;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION pagination(limit_value int, offset_value int)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    type VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    ORDER BY c.id
    LIMIT limit_value
    OFFSET offset_value;
END;
$$ LANGUAGE plpgsql;