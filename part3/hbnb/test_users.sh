#!/bin/bash

echo "Starting HBnB server..."
python3 run.py &

SERVER_PID=$!
sleep 3

echo ""
echo "=============================="
echo "TEST 1: Create User (POST)"
echo "=============================="

CREATE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "email":"script@test.com",
  "password":"123456",
  "first_name":"Nada",
  "last_name":"Initial"
}')

echo "$CREATE_RESPONSE"

USER_ID=$(echo $CREATE_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo ""
echo "=============================="
echo "TEST 2: Get User (GET)"
echo "=============================="

curl -s http://127.0.0.1:5000/api/v1/users/$USER_ID

echo ""
echo ""
echo "=============================="
echo "TEST 3: Update User (PUT)"
echo "=============================="

curl -s -X PUT http://127.0.0.1:5000/api/v1/users/$USER_ID \
-H "Content-Type: application/json" \
-d '{
  "first_name":"Nada Updated",
  "last_name":"HBnB"
}'

echo ""
echo ""
echo "Stopping server..."
kill $SERVER_PID

