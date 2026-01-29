#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/v1"

EMAIL="users_test_$(date +%s)@example.com"
PASSWORD="user123"

echo "=============================="
echo " USERS FULL TEST STARTED"
echo "=============================="

echo "== LOGIN ADMIN =="
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}')

ADMIN_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$ADMIN_LOGIN""")["access_token"])
EOF
)

AUTH_ADMIN="Authorization: Bearer $ADMIN_TOKEN"

echo
echo "== CREATE USER =="
CREATE_USER=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_ADMIN" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\",
    \"first_name\": \"Test\",
    \"last_name\": \"User\"
  }")

#echo "$CREATE_USER"

#USER_ID=$(python3 - <<EOF
#import json
#print(json.loads("""$CREATE_USER""")["id"])
#EOF
#)

echo
echo "== LOGIN USER =="
USER_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

USER_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$USER_LOGIN""")["access_token"])
EOF
)

AUTH_USER="Authorization: Bearer $USER_TOKEN"

echo
echo "== GET USER (SELF) =="
curl -s -X GET $BASE_URL/users/$USER_ID \
  -H "$AUTH_USER"

echo
echo "== UPDATE USER (SELF) =="
curl -s -X PUT $BASE_URL/users/$USER_ID \
  -H "Content-Type: application/json" \
  -H "$AUTH_USER" \
  -d '{"first_name":"Updated"}'

echo
echo "== USER CANNOT LIST USERS =="
curl -s -X GET $BASE_URL/users/ \
  -H "$AUTH_USER"

echo
echo "== ADMIN LIST USERS =="
curl -s -X GET $BASE_URL/users/ \
  -H "$AUTH_ADMIN"

echo
echo "== USER CANNOT EDIT OTHER USER =="
curl -s -X PUT $BASE_URL/users/00000000-0000-0000-0000-000000000000 \
  -H "Content-Type: application/json" \
  -H "$AUTH_USER" \
  -d '{"first_name":"Hack"}'

echo
echo "== GET NON-EXISTENT USER =="
curl -s -X GET $BASE_URL/users/00000000-0000-0000-0000-000000000000 \
  -H "$AUTH_ADMIN"

echo
echo "=============================="
echo " USERS FULL TEST COMPLETED"
echo "=============================="
