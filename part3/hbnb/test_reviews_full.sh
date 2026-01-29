#!/usr/bin/env bash

set -e

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=============================="
echo " REVIEWS FULL TEST STARTED"
echo "=============================="

# ------------------------------
# LOGIN ADMIN
# ------------------------------
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}')

ADMIN_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$ADMIN_LOGIN""")["access_token"])
EOF
)

AUTH_ADMIN="Authorization: Bearer $ADMIN_TOKEN"

# ------------------------------
# CREATE PLACE OWNER (User A)
# ------------------------------
OWNER_EMAIL="owner_$(date +%s)@example.com"

curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_ADMIN" \
  -d "{
    \"email\": \"$OWNER_EMAIL\",
    \"password\": \"owner123\",
    \"first_name\": \"Place\",
    \"last_name\": \"Owner\"
  }" > /dev/null

OWNER_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$OWNER_EMAIL\",\"password\":\"owner123\"}")

OWNER_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$OWNER_LOGIN""")["access_token"])
EOF
)

AUTH_OWNER="Authorization: Bearer $OWNER_TOKEN"

# ------------------------------
# CREATE PLACE (by Owner)
# ------------------------------
PLACE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_OWNER" \
  -d '{
    "title": "Review Test Place",
    "description": "Nice place",
    "price_per_night": 120
  }')

PLACE_ID=$(python3 - <<EOF
import json
print(json.loads("""$PLACE""")["id"])
EOF
)

# ------------------------------
# CREATE REVIEWER (User B)
# ------------------------------
REVIEWER_EMAIL="reviewer_$(date +%s)@example.com"

curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_ADMIN" \
  -d "{
    \"email\": \"$REVIEWER_EMAIL\",
    \"password\": \"reviewer123\",
    \"first_name\": \"Review\",
    \"last_name\": \"User\"
  }" > /dev/null

REVIEWER_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$REVIEWER_EMAIL\",\"password\":\"reviewer123\"}")

REVIEWER_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$REVIEWER_LOGIN""")["access_token"])
EOF
)

AUTH_REVIEWER="Authorization: Bearer $REVIEWER_TOKEN"

# ------------------------------
# CREATE REVIEW
# ------------------------------
echo "== CREATE REVIEW =="

REVIEW=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_REVIEWER" \
  -d "{
    \"place_id\": \"$PLACE_ID\",
    \"rating\": 5,
    \"text\": \"Amazing place\"
  }")

echo "$REVIEW"

REVIEW_ID=$(python3 - <<EOF
import json
print(json.loads("""$REVIEW""")["id"])
EOF
)

# ------------------------------
# GET REVIEW
# ------------------------------
echo "== GET REVIEW =="

curl -s -X GET $BASE_URL/reviews/$REVIEW_ID

# ------------------------------
# UPDATE REVIEW
# ------------------------------
echo "== UPDATE REVIEW =="

curl -s -X PUT $BASE_URL/reviews/$REVIEW_ID \
  -H "Content-Type: application/json" \
  -H "$AUTH_REVIEWER" \
  -d '{
    "text": "Updated review",
    "rating": 4
  }'

# ------------------------------
# DELETE REVIEW
# ------------------------------
echo "== DELETE REVIEW =="

curl -s -X DELETE $BASE_URL/reviews/$REVIEW_ID \
  -H "$AUTH_REVIEWER"

# ------------------------------
# GET REVIEW AFTER DELETE
# ------------------------------
echo "== GET REVIEW AFTER DELETE =="

curl -s -X GET $BASE_URL/reviews/$REVIEW_ID

echo ""
echo "=============================="
echo " REVIEWS FULL TEST COMPLETED"
echo "=============================="
