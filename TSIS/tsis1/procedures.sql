CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    -- check if contact exists
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_name;

    IF v_contact_id IS NOT NULL THEN
        -- update phone (replace existing phones)
        DELETE FROM phones WHERE contact_id = v_contact_id;

        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, 'mobile');

    ELSE
        -- create new contact
        INSERT INTO contacts (name, group_id)
        VALUES (p_name, 4)  -- default group: Other
        RETURNING id INTO v_contact_id;

        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, 'mobile');
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    v_contact_id INT;
BEGIN
    FOR i IN 1..array_length(names,1) LOOP

        -- validate phone
        IF phones[i] ~ '^[0-9+]+$' THEN

            -- create contact
            INSERT INTO contacts (name, group_id)
            VALUES (names[i], 4)
            RETURNING id INTO v_contact_id;

            -- insert phone
            INSERT INTO phones (contact_id, phone, type)
            VALUES (v_contact_id, phones[i], 'mobile');

        ELSE
            RAISE NOTICE 'Incorrect data: %, %', names[i], phones[i];
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN

    -- delete by birthday
    IF p_value ~ '^\d{4}-\d{2}-\d{2}$' THEN
        DELETE FROM contacts
        WHERE birthday = p_value::DATE;

    -- delete by email
    ELSIF p_value LIKE '%@%' THEN
        DELETE FROM contacts
        WHERE email = p_value;

    -- delete by id (strict number, short)
    ELSIF p_value ~ '^[0-9]+$' AND length(p_value) <= 5 THEN
        DELETE FROM contacts
        WHERE id = p_value::INT;

    -- delete by phone (long number or +)
    ELSIF p_value ~ '^[0-9+]+$' THEN
        DELETE FROM contacts
        WHERE id IN (
            SELECT contact_id FROM phones WHERE phone = p_value
        );

    -- delete by name
    ELSE
        DELETE FROM contacts
        WHERE name = p_value;
    END IF;

    IF NOT FOUND THEN
        RAISE NOTICE 'Contact not found';
    END IF;

END;
$$;

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_id INT,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- check contact exists
    IF NOT EXISTS (SELECT 1 FROM contacts WHERE id = p_contact_id) THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    -- validate type
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE NOTICE 'Invalid phone type';
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (p_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_id INT,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- check contact exists
    IF NOT EXISTS (SELECT 1 FROM contacts WHERE id = p_contact_id) THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    -- find or create group
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name)
        VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = p_contact_id;
END;
$$;