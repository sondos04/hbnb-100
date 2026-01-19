#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"
API_BASE="${API_BASE:-$BASE_URL/api/v1}"

echo "== HBnB Places + Reviews Test =="
echo "BASE_URL: $BASE_URL"
echo "API_BASE:  $API_BASE"
echo

# ---------- helpers ----------
req() {
  # usage: req METHOD URL JSON(optional)
  local method="$1"
  local url="$2"
  local data="${3:-}"

  if [[ -n "$data" ]]; then
    curl -sS -i -X "$method" "$url" \
      -H "Content-Type: application/json" \
      -d "$data"
  else
    curl -sS -i -X "$method" "$url"
  fi
}

status_code() {
  awk 'BEGIN{code=""}
       /^HTTP\/1\.[01]/{gsub("\r",""); code=$2}
       END{print code}'
}

body_only() {
  awk 'BEGIN{h=1}
       {sub("\r$","")}
       { if(h && $0=="") {h=0; next} }
       { if(!h) print }'
}


json_get() {
  local key="$1"
  python3 - <<'PY'
import sys, json, re

text = sys.stdin.read()

# extract first JSON object
m = re.search(r'\{.*\}', text, re.S)
if not m:
    print("")
    sys.exit(0)

try:
    obj = json.loads(m.group(0))
    print(obj.get(sys.argv[1], ""))
except Exception:
    print("")
PY
}

assert_status() {
  local got="$1"
  local want="$2"
  local msg="$3"
  if [[ "$got" != "$want" ]]; then
    echo "$msg"
    echo "   expected: $want"
    echo "   got:      $got"
    exit 1
  fi
  echo "$msg ($got)"
}

# ---------- 0) smoke tests ----------
echo "== 0) Smoke Tests =="
RESP="$(req GET "$API_BASE/places/")"
CODE="$(printf "%s" "$RESP" | status_code)"
assert_status "$CODE" "200" "GET /places/"

RESP="$(req GET "$API_BASE/reviews/")"
CODE="$(printf "%s" "$RESP" | status_code)"
assert_status "$CODE" "200" "GET /reviews/"
echo

# ---------- 1) create user ----------
echo "== 1) Create User =="
RAND="$(python3 - <<'PY'
import uuid
print(uuid.uuid4().hex[:8])
PY
)"
EMAIL="test_${RAND}@example.com"
USER_PAYLOAD="$(cat <<JSON
{
  "email": "$EMAIL",
  "password": "Passw0rd!",
  "first_name": "Test",
  "last_name": "User"
}
JSON
)"

RESP="$(req POST "$API_BASE/users/" "$USER_PAYLOAD")"
CODE="$(printf "%s" "$RESP" | status_code)"
BODY="$(printf "%s" "$RESP" | body_only)"
# Some projects return 201, some 200. Accept both.
if [[ "$CODE" != "201" && "$CODE" != "200" ]]; then
  echo "Create user failed (expected 200 or 201, got $CODE)"
  echo "$BODY"
  exit 1
fi
echo "POST /users/ ($CODE)"
USER_ID="$(printf "%s" "$BODY" | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')"
if [[ -z "$USER_ID" ]]; then
  echo "Could not extract USER_ID from response body:"
  echo "$BODY"
  exit 1
fi
echo "USER_ID: $USER_ID"
echo

# ---------- 2) create place ----------
echo "== 2) Create Place =="
PLACE_PAYLOAD="$(cat <<JSON
{
  "title": "My First Place",
  "owner_id": "$USER_ID",
  "description": "Nice place",
  "price_per_night": 120
}
JSON
)"
RESP="$(req POST "$API_BASE/places/" "$PLACE_PAYLOAD")"
CODE="$(printf "%s" "$RESP" | status_code)"
BODY="$(printf "%s" "$RESP" | body_only)"
assert_status "$CODE" "201" "POST /places/"
PLACE_ID="$(printf "%s" "$BODY" | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')"
if [[ -z "$PLACE_ID" ]]; then
  echo "Could not extract PLACE_ID from response body:"
  echo "$BODY"
  exit 1
fi
echo "PLACE_ID: $PLACE_ID"
echo

echo "== 3) Get Place By ID =="
RESP="$(req GET "$API_BASE/places/$PLACE_ID")"
CODE="$(printf "%s" "$RESP" | status_code)"
assert_status "$CODE" "200" "GET /places/<id>"
echo

# ---------- 4) create review ----------
echo "== 4) Create Review =="
REVIEW_PAYLOAD="$(cat <<JSON
{
  "text": "Great place!",
  "user_id": "$USER_ID",
  "place_id": "$PLACE_ID",
  "rating": 5
}
JSON
)"
RESP="$(req POST "$API_BASE/reviews/" "$REVIEW_PAYLOAD")"
CODE="$(printf "%s" "$RESP" | status_code)"
BODY="$(printf "%s" "$RESP" | body_only)"
assert_status "$CODE" "201" "POST /reviews/"
REVIEW_ID="$(printf "%s" "$BODY" | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')"
if [[ -z "$REVIEW_ID" ]]; then
  echo "Could not extract REVIEW_ID from response body:"
  echo "$BODY"
  exit 1
fi
echo "REVIEW_ID: $REVIEW_ID"
echo

# ---------- 5) duplicate review should fail ----------
echo "== 5) Duplicate Review Must Fail =="
DUP_PAYLOAD="$(cat <<JSON
{
  "text": "Duplicate review attempt",
  "user_id": "$USER_ID",
  "place_id": "$PLACE_ID",
  "rating": 4
}
JSON
)"
RESP="$(req POST "$API_BASE/reviews/" "$DUP_PAYLOAD")"
CODE="$(printf "%s" "$RESP" | status_code)"
BODY="$(printf "%s" "$RESP" | body_only)"

# Expected 400 (your API uses ValueError -> abort(400,...))
assert_status "$CODE" "400" "POST /reviews/ duplicate (should be 400)"
echo "Message: $(printf "%s" "$BODY" | json_get message)"
echo

# ---------- 6) get all reviews ----------
echo "== 6) Get All Reviews =="
RESP="$(req GET "$API_BASE/reviews/")"
CODE="$(printf "%s" "$RESP" | status_code)"
assert_status "$CODE" "200" "GET /reviews/"
echo

# ---------- 7) get review by id (if endpoint exists) ----------
echo "== 7) Get Review By ID (if enabled) =="
RESP="$(req GET "$API_BASE/reviews/$REVIEW_ID")"
CODE="$(printf "%s" "$RESP" | status_code)"
if [[ "$CODE" == "200" ]]; then
  echo "GET /reviews/<id> ($CODE)"
else
  echo "GET /reviews/<id> returned $CODE (this is OK if you didn't add the endpoint)."
fi

echo
echo "All core Places + Reviews tests completed."

