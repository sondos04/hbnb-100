#!/bin/bash

echo "Starting server..."
python3 run.py &
SERVER_PID=$!
sleep 2

echo "=============================="
echo "TASK 3: Create Amenity (POST)"
echo "=============================="
AMENITY_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}')

echo "$AMENITY_RESPONSE"

AMENITY_ID=$(echo "$AMENITY_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo
echo "=============================="
echo "TASK 3: Get Amenity by ID (GET)"
echo "=============================="
curl -s http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID
echo

echo
echo "=============================="
echo "TASK 4: Update Amenity (PUT)"
echo "=============================="
curl -s -X PUT http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID \
-H "Content-Type: application/json" \
-d '{"name":"Updated WiFi"}'
echo

echo
echo "=============================="
echo "TASK 5: Create User for Place"
echo "=============================="
USER_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"email":"place@test.com","password":"123456","first_name":"Nada","last_name":"Place"}')

echo "$USER_RESPONSE"

USER_ID=$(echo "$USER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo
echo "=============================="
echo "TASK 5: Create Place (POST)"
echo "=============================="
PLACE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d "{
  \"title\":\"Test Place\",
  \"owner_id\":\"$USER_ID\",
  \"description\":\"Nice place\",
  \"price_per_night\":100
}")

echo "$PLACE_RESPONSE"

PLACE_ID=$(echo "$PLACE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo
echo "=============================="
echo "TASK 6: Get Place by ID (GET)"
echo "=============================="
curl -s http://127.0.0.1:5000/api/v1/places/$PLACE_ID
echo

echo
echo "Stopping server..."
kill $SERVER_PID

