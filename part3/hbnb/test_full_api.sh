#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:80}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@hbnb.io}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"
CURL="curl -s -i"

hr() { echo -e "\n============================================================\n"; }
title() { hr; echo "### $1"; hr; }

# Extract JSON field from a response (best-effort without jq)
extract_json_field() {
  # usage: extract_json_field "field_name" <<< "$response"
  local field="$1"
  # grab last JSON line(s), then find "field":"value"
  echo "$1" >/dev/null 2>&1 || true
}

get_body() {
  # prints body only
  awk 'BEGIN{p=0} /^\r?$/{p=1; next} {if(p) print}' | sed 's/\r$//'
}

get_status() {
  # prints HTTP status code
  head -n 1 | awk '{print $2}'
}

json_get() {
  # very small JSON getter: json_get key  (expects "key":"value" in body)
  local key="$1"
  get_body | tr -d '\n' | sed -n "s/.*\"$key\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p"
}

echo "BASE_URL=$BASE_URL"
echo "Using admin login: $ADMIN_EMAIL"

title "0) Swagger page reachable"
$CURL "$BASE_URL/api/v1/" | head -n 15

title "1) AUTH: Login success -> get JWT token"
LOGIN_RES="$($CURL -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}")"

echo "$LOGIN_RES" | head -n 20
TOKEN="$(echo "$LOGIN_RES" | json_get access_token)"
if [[ -z "${TOKEN}" ]]; then
  echo "ERROR: Could not extract access_token from login response."
  echo "Tip: If your login returns a different field name, edit: json_get access_token"
  exit 1
fi
echo -e "\nExtracted TOKEN (first 30 chars): ${TOKEN:0:30}..."

title "2) USERS: GET all users (admin auth required)"
$CURL "$BASE_URL/api/v1/users/" -H "Authorization: Bearer $TOKEN"

title "3) USERS: Create user (valid)"
USER_CREATE_RES="$($CURL -X POST "$BASE_URL/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test1@hbnb.io","password":"123456","first_name":"Test","last_name":"User"}')"
echo "$USER_CREATE_RES"
USER_ID="$(echo "$USER_CREATE_RES" | json_get id)"
echo -e "\nUSER_ID=$USER_ID"

title "4) USERS: Create user (duplicate email -> expect 400)"
$CURL -X POST "$BASE_URL/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test1@hbnb.io","password":"123456","first_name":"X","last_name":"Y"}'

title "5) USERS: Update user (valid)"
$CURL -X PUT "$BASE_URL/api/v1/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"ApiUpdated","last_name":"UserUpdated"}'

title "6) USERS: Update user (invalid first_name whitespace -> expect 400)"
$CURL -X PUT "$BASE_URL/api/v1/users/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"   "}'

title "7) AMENITIES: Create amenity WiFi (valid)"
AM1_RES="$($CURL -X POST "$BASE_URL/api/v1/amenities/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"WiFi"}')"
echo "$AM1_RES"
AMENITY_ID="$(echo "$AM1_RES" | json_get id)"
echo -e "\nAMENITY_ID=$AMENITY_ID"

title "8) AMENITIES: Create amenity (empty name -> expect 400)"
$CURL -X POST "$BASE_URL/api/v1/amenities/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":""}'

title "9) AMENITIES: Get all amenities"
$CURL "$BASE_URL/api/v1/amenities/"

title "10) PLACES: Create place (valid)"
# Prefer using ADMIN user id if it's in DB; otherwise use the created USER_ID
OWNER_ID="${OWNER_ID:-00000000-0000-0000-0000-000000000001}"
PLACE_CREATE_RES="$($CURL -X POST "$BASE_URL/api/v1/places/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\":\"Villa\",
    \"description\":\"Nice place\",
    \"price\":150,
    \"latitude\":24.7,
    \"longitude\":46.7,
    \"owner_id\":\"$OWNER_ID\",
    \"amenities\":[\"$AMENITY_ID\"]
  }")"
echo "$PLACE_CREATE_RES"
PLACE_ID="$(echo "$PLACE_CREATE_RES" | json_get id)"
echo -e "\nPLACE_ID=$PLACE_ID"

title "11) PLACES: Create place (invalid negative price -> expect 400)"
$CURL -X POST "$BASE_URL/api/v1/places/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\":\"Bad\",
    \"price\":-10,
    \"latitude\":0,
    \"longitude\":0,
    \"owner_id\":\"$OWNER_ID\",
    \"amenities\":[]
  }"

title "12) PLACES: Get all places (basic)"
$CURL "$BASE_URL/api/v1/places/"

title "13) PLACES: Get place by id (full)"
$CURL "$BASE_URL/api/v1/places/$PLACE_ID"

title "14) PLACES: Update place (valid price update)"
$CURL -X PUT "$BASE_URL/api/v1/places/$PLACE_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price":200}'

title "15) REVIEWS: Create review (valid)"
REVIEW_CREATE_RES="$($CURL -X POST "$BASE_URL/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\":\"Amazing\",
    \"rating\":5,
    \"user_id\":\"$OWNER_ID\",
    \"place_id\":\"$PLACE_ID\"
  }")"
echo "$REVIEW_CREATE_RES"
REVIEW_ID="$(echo "$REVIEW_CREATE_RES" | json_get id)"
echo -e "\nREVIEW_ID=$REVIEW_ID"

title "16) REVIEWS: Create review (invalid rating -> expect 400)"
$CURL -X POST "$BASE_URL/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\":\"Bad\",
    \"rating\":10,
    \"user_id\":\"$OWNER_ID\",
    \"place_id\":\"$PLACE_ID\"
  }"

title "17) REVIEWS: Get review by id"
$CURL "$BASE_URL/api/v1/reviews/$REVIEW_ID"

title "18) REVIEWS: Get reviews by place"
$CURL "$BASE_URL/api/v1/places/$PLACE_ID/reviews"

title "19) REVIEWS: Update review"
$CURL -X PUT "$BASE_URL/api/v1/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Updated","rating":4}'

title "20) REVIEWS: Delete review"
$CURL -X DELETE "$BASE_URL/api/v1/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $TOKEN"

title "21) REVIEWS: Get deleted review (expect 404)"
$CURL "$BASE_URL/api/v1/reviews/$REVIEW_ID"

hr
echo "✅ DONE: Full API test script completed."
