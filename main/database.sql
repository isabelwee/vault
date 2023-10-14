-- create the users table 
CREATE TABLE IF NOT EXISTS Vault (
    app_name    TEXT PRIMARY KEY    NOT NULL,
    url         TEXT,
    username    TEXT,
    user_email  TEXT,
    password    TEXT 
);


-- -- ensures that either username or user-email is filled in
-- CREATE OR REPLACE FUNCTION check_user_not_null()
-- RETURN TRIGGER AS $$
-- BEGIN
--     IF NEW.username IS NULL AND NEW.user_email IS NULL THEN
--         RAISE EXCEPTION 'Both username and user_email cannot be NULL';
--     END IF;
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER check_user_not_null
-- BEFORE INSERT ON Vault
-- FOR EACH ROW
-- EXECUTE FUNCTION check_user_not_null();
