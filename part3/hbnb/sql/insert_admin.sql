DELETE FROM users WHERE email = 'admin@hbnb.io';

INSERT INTO users (
    id, email, password, first_name, last_name, is_admin, created_at, updated_at
) VALUES (
    '00000000-0000-0000-0000-000000000001',
    'admin@hbnb.io',
    '$2b$12$oJts4jSRERjf4K5GlI/9qeac2YRhRkAaz6/TmgjcqAY2rwBwsH2k6',
    'Admin',
    'User',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
