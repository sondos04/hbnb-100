-- ✅ FIXED: Using actual UUIDs instead of UUID() function (SQLite doesn't support UUID())
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES
    ('a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
