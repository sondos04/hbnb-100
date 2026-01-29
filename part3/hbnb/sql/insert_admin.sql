DELETE FROM users WHERE email = 'admin@hbnb.io';

-- ✅ FIXED: Using task-specified UUID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1
INSERT INTO users (
    id, email, password, first_name, last_name, is_admin, created_at, updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    '$2b$12$oJts4jSRERjf4K5GlI/9qeac2YRhRkAaz6/TmgjcqAY2rwBwsH2k6',
    'Admin',
    'HBnB',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
