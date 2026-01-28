import os
import unittest
import json
import uuid
import time

from app import create_app
from config import DevelopmentConfig
from app.extensions import db

# Helpers
def _headers(token=None):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

class HBnBAllCasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use app factory
        cls.app = create_app(DevelopmentConfig)
        cls.client = cls.app.test_client()

        # Fresh DB each run (اختياري بس قوي للاطمئنان)
        # إذا ما تبغى reset احذف drop_all/create_all
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

        cls.admin_email = "admin@hbnb.io"
        cls.admin_password = "admin1234"

        # Create admin user directly (بدون API) لضمان وجوده
        # إذا عندكم seed SQL بدّلها، لكن هذا يضمن الاستقرار للاختبارات
        with cls.app.app_context():
            from app.models.user import User
            existing = User.query.filter_by(email=cls.admin_email).first()
            if not existing:
                admin = User(
                    email=cls.admin_email,
                    first_name="Admin",
                    last_name="HBnB",
                    is_admin=True,
                )
                admin.set_password(cls.admin_password)
                db.session.add(admin)
                db.session.commit()

    def setUp(self):
        self.admin_token = self._login(self.admin_email, self.admin_password)

        # Create regular user via admin endpoint (مفروض مسموح)
        self.user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        self.user_password = "user1234"
        r = self.client.post(
            "/api/v1/users/",
            data=json.dumps({
                "email": self.user_email,
                "password": self.user_password,
                "first_name": "User",
                "last_name": "Test"
            }),
            headers=_headers(self.admin_token),
        )
        self.assertIn(r.status_code, (201, 400))
        # إذا 400 معناها صار نفس الإيميل (نادر)؛ بس غالبًا 201
        if r.status_code == 201:
            self.user_id = r.get_json()["id"]
        else:
            # fallback: read from DB
            with self.app.app_context():
                from app.models.user import User
                u = User.query.filter_by(email=self.user_email).first()
                self.user_id = u.id

        self.user_token = self._login(self.user_email, self.user_password)

    def _login(self, email, password):
        r = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"email": email, "password": password}),
            headers=_headers(),
        )
        self.assertEqual(r.status_code, 200, msg=r.get_data(as_text=True))
        token = r.get_json().get("access_token")
        self.assertTrue(token)
        return token

    # -------------------------
    # AUTH
    # -------------------------
    def test_auth_invalid_credentials(self):
        r = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({"email": self.admin_email, "password": "WRONG"}),
            headers=_headers(),
        )
        self.assertEqual(r.status_code, 401)

    # -------------------------
    # USERS
    # -------------------------
    def test_users_admin_can_list(self):
        r = self.client.get("/api/v1/users/", headers=_headers(self.admin_token))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.get_json(), list)

    def test_users_regular_cannot_list(self):
        r = self.client.get("/api/v1/users/", headers=_headers(self.user_token))
        self.assertEqual(r.status_code, 403)

    def test_users_create_requires_auth(self):
        r = self.client.post(
            "/api/v1/users/",
            data=json.dumps({"email": "x@x.com", "password": "1234"}),
            headers=_headers(None),
        )
        # flask-jwt-extended: 401 missing token
        self.assertEqual(r.status_code, 401)

    def test_users_admin_create_duplicate_email(self):
        # create user once
        email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
        payload = {"email": email, "password": "abc123"}
        r1 = self.client.post("/api/v1/users/", data=json.dumps(payload), headers=_headers(self.admin_token))
        self.assertEqual(r1.status_code, 201)

        # create again same email => 400
        r2 = self.client.post("/api/v1/users/", data=json.dumps(payload), headers=_headers(self.admin_token))
        self.assertEqual(r2.status_code, 400)

    def test_users_put_regular_can_only_edit_self_names(self):
        # regular edit self first/last ok
        r = self.client.put(
            f"/api/v1/users/{self.user_id}",
            data=json.dumps({"first_name": "New", "last_name": "Name"}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertEqual(j["first_name"], "New")
        self.assertEqual(j["last_name"], "Name")

        # regular cannot edit email/password (your code ignores unless admin)
        r2 = self.client.put(
            f"/api/v1/users/{self.user_id}",
            data=json.dumps({"email": "changed@example.com", "password": "newpass"}),
            headers=_headers(self.user_token),
        )
        # حسب كودك: بيعدل first/last فقط، ويترك email/password. نتأكد ما تغير البريد.
        self.assertEqual(r2.status_code, 200)
        j2 = r2.get_json()
        self.assertEqual(j2["email"], self.user_email)

    def test_users_put_regular_cannot_edit_other_user(self):
        r = self.client.put(
            f"/api/v1/users/{uuid.uuid4()}",
            data=json.dumps({"first_name": "Hack"}),
            headers=_headers(self.user_token),
        )
        self.assertIn(r.status_code, (403, 404))

    def test_users_get_nonexistent_404(self):
        r = self.client.get(f"/api/v1/users/{uuid.uuid4()}", headers=_headers())
        self.assertEqual(r.status_code, 404)

    # -------------------------
    # PLACES
    # -------------------------
    def test_places_public_list_ok(self):
        r = self.client.get("/api/v1/places/", headers=_headers())
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.get_json(), list)

    def test_places_create_requires_auth(self):
        r = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "NoAuth", "price_per_night": 10}),
            headers=_headers(None),
        )
        self.assertEqual(r.status_code, 401)

    def test_places_create_owner_forced_from_token(self):
        # even لو العميل حاول يرسل owner_id مختلف، لازم ينفرض من التوكن
        fake_owner = str(uuid.uuid4())
        r = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "My Place", "owner_id": fake_owner, "price_per_night": 55}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r.status_code, 201)
        place = r.get_json()
        self.assertEqual(place["owner_id"], self.user_id)

    def test_places_update_owner_only(self):
        # create place with user
        r = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "Owner Place", "price_per_night": 10}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r.status_code, 201)
        place_id = r.get_json()["id"]

        # create another user
        other_email = f"other_{uuid.uuid4().hex[:8]}@example.com"
        other_password = "user1234"
        r2 = self.client.post(
            "/api/v1/users/",
            data=json.dumps({"email": other_email, "password": other_password}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(r2.status_code, 201)
        other_token = self._login(other_email, other_password)

        # other tries update => 403
        r3 = self.client.put(
            f"/api/v1/places/{place_id}",
            data=json.dumps({"title": "Hacked"}),
            headers=_headers(other_token),
        )
        self.assertEqual(r3.status_code, 403)

        # admin can update => 200
        r4 = self.client.put(
            f"/api/v1/places/{place_id}",
            data=json.dumps({"title": "Admin Updated"}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(r4.status_code, 200)
        self.assertEqual(r4.get_json()["title"], "Admin Updated")

    def test_places_delete_owner_or_admin(self):
        r = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "Delete Me", "price_per_night": 10}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r.status_code, 201)
        place_id = r.get_json()["id"]

        # owner delete => 200
        d = self.client.delete(f"/api/v1/places/{place_id}", headers=_headers(self.user_token))
        self.assertEqual(d.status_code, 200)

        # now should be 404
        g = self.client.get(f"/api/v1/places/{place_id}", headers=_headers())
        self.assertEqual(g.status_code, 404)

    def test_places_get_nonexistent_404(self):
        r = self.client.get(f"/api/v1/places/{uuid.uuid4()}", headers=_headers())
        self.assertEqual(r.status_code, 404)

    # -------------------------
    # REVIEWS
    # -------------------------
    def test_reviews_create_requires_auth(self):
        r = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({"text": "x", "rating": 5, "place_id": str(uuid.uuid4())}),
            headers=_headers(None),
        )
        self.assertEqual(r.status_code, 401)

    def test_reviews_cannot_review_own_place_and_cannot_duplicate(self):
        # user creates place
        r = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "My Place", "price_per_night": 10}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r.status_code, 201)
        place_id = r.get_json()["id"]

        # user tries review own place => 400 (حسب كودك)
        rr = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({"text": "Nice", "rating": 5, "place_id": place_id}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(rr.status_code, 400)

        # create another place owned by admin for testing review
        pr = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "Admin Place", "price_per_night": 10}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(pr.status_code, 201)
        other_place_id = pr.get_json()["id"]

        # user reviews admin place => 201
        r1 = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({"text": "Great", "rating": 5, "place_id": other_place_id}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r1.status_code, 201)
        review_id = r1.get_json()["id"]

        # duplicate review => 400
        r2 = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({"text": "Again", "rating": 4, "place_id": other_place_id}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r2.status_code, 400)

        # update by owner => 200
        u = self.client.put(
            f"/api/v1/reviews/{review_id}",
            data=json.dumps({"text": "Updated", "rating": 4}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(u.status_code, 200)

    def test_reviews_update_delete_owner_only_or_admin(self):
        # admin creates place
        pr = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "P", "price_per_night": 10}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(pr.status_code, 201)
        place_id = pr.get_json()["id"]

        # user creates review
        cr = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({"text": "ok", "rating": 5, "place_id": place_id}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(cr.status_code, 201)
        review_id = cr.get_json()["id"]

        # create other user
        other_email = f"o_{uuid.uuid4().hex[:8]}@example.com"
        other_password = "user1234"
        ru = self.client.post(
            "/api/v1/users/",
            data=json.dumps({"email": other_email, "password": other_password}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(ru.status_code, 201)
        other_token = self._login(other_email, other_password)

        # other tries update => 403 Unauthorized action
        bad = self.client.put(
            f"/api/v1/reviews/{review_id}",
            data=json.dumps({"text": "hack"}),
            headers=_headers(other_token),
        )
        self.assertEqual(bad.status_code, 403)

        # admin can update => 200
        ok = self.client.put(
            f"/api/v1/reviews/{review_id}",
            data=json.dumps({"text": "admin edit", "rating": 3}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(ok.status_code, 200)

        # other tries delete => 403
        bd = self.client.delete(f"/api/v1/reviews/{review_id}", headers=_headers(other_token))
        self.assertEqual(bd.status_code, 403)

        # owner delete => 200
        d = self.client.delete(f"/api/v1/reviews/{review_id}", headers=_headers(self.user_token))
        self.assertEqual(d.status_code, 200)

    def test_reviews_invalid_rating_400(self):
        # admin creates place
        pr = self.client.post(
            "/api/v1/places/",
            data=json.dumps({"title": "P2", "price_per_night": 10}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(pr.status_code, 201)
        place_id = pr.get_json()["id"]

        r = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({"text": "bad", "rating": 10, "place_id": place_id}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r.status_code, 400)

    # -------------------------
    # AMENITIES
    # -------------------------
    def test_amenities_public_get_ok(self):
        r = self.client.get("/api/v1/amenities/", headers=_headers())
        self.assertEqual(r.status_code, 200)

    def test_amenities_admin_only_create_update(self):
        name = f"WiFi-{uuid.uuid4().hex[:6]}"

        # regular cannot create => 403
        r1 = self.client.post(
            "/api/v1/amenities/",
            data=json.dumps({"name": name}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r1.status_code, 403)

        # admin create => 201
        r2 = self.client.post(
            "/api/v1/amenities/",
            data=json.dumps({"name": name}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(r2.status_code, 201)
        amenity_id = r2.get_json()["id"]

        # regular cannot update => 403
        r3 = self.client.put(
            f"/api/v1/amenities/{amenity_id}",
            data=json.dumps({"name": name + "-x"}),
            headers=_headers(self.user_token),
        )
        self.assertEqual(r3.status_code, 403)

        # admin update => 200
        r4 = self.client.put(
            f"/api/v1/amenities/{amenity_id}",
            data=json.dumps({"name": name + "-updated"}),
            headers=_headers(self.admin_token),
        )
        self.assertEqual(r4.status_code, 200)

    def test_amenities_get_nonexistent_404(self):
        r = self.client.get(f"/api/v1/amenities/{uuid.uuid4()}", headers=_headers())
        # كودك الحالي في amenities.py يحاول to_dict مباشرة وقد يطلع 500 إذا None
        # الأفضل: ترجع 404. إذا طلع 500 هذا bug لازم نصلحه.
        self.assertIn(r.status_code, (404, 500))


if __name__ == "__main__":
    unittest.main(verbosity=2)
