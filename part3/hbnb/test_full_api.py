# part3/tests/test_full_api.py

import os
import unittest

from app import create_app
from config import DevelopmentConfig
from app.extensions import db

# Import models to ensure tables/relationships load
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestConfig(DevelopmentConfig):
    TESTING = True
    # DB file isolated للاختبارات (ما يلخبط development.db)
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_hbnb.db"


class HBnBFullAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure clean db file
        # (sqlite:///test_hbnb.db غالبًا ينحط داخل part3/)
        db_path = "test_hbnb.db"
        if os.path.exists(db_path):
            os.remove(db_path)

        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

            # Create Admin directly in DB (because POST /users is admin-only)
            admin = User(
                email="admin@hbnb.io",
                first_name="Admin",
                last_name="HBnB",
                is_admin=True
            )
            admin.set_password("admin1234")
            db.session.add(admin)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

        db_path = "test_hbnb.db"
        if os.path.exists(db_path):
            os.remove(db_path)

    # -------------------------
    # Helpers
    # -------------------------
    def login(self, email, password):
        res = self.client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        self.assertEqual(res.status_code, 200, res.get_json())
        data = res.get_json()
        self.assertIn("access_token", data)
        return data["access_token"]

    def auth_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    # -------------------------
    # Tests
    # -------------------------
    def test_01_auth_login_admin_success(self):
        token = self.login("admin@hbnb.io", "admin1234")
        self.assertTrue(token)

    def test_02_users_admin_create_and_list(self):
        admin_token = self.login("admin@hbnb.io", "admin1234")

        # Create user via admin-only endpoint
        res = self.client.post(
            "/api/v1/users/",
            json={
                "email": "user1@test.com",
                "password": "pass1234",
                "first_name": "User",
                "last_name": "One",
            },
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        user = res.get_json()
        self.assertIn("id", user)
        user_id = user["id"]

        # Get user public endpoint (no token required)
        res = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(res.status_code, 200, res.get_json())
        body = res.get_json()
        self.assertEqual(body["email"], "user1@test.com")
        self.assertNotIn("password", body)  # ensure password never returned

        # List users admin-only
        res = self.client.get("/api/v1/users/", headers=self.auth_headers(admin_token))
        self.assertEqual(res.status_code, 200, res.get_json())
        users = res.get_json()
        self.assertTrue(isinstance(users, list))
        self.assertTrue(any(u["email"] == "user1@test.com" for u in users))

    def test_03_users_regular_cannot_create(self):
        admin_token = self.login("admin@hbnb.io", "admin1234")

        # create normal user first
        res = self.client.post(
            "/api/v1/users/",
            json={
                "email": "user2@test.com",
                "password": "pass1234",
                "first_name": "User",
                "last_name": "Two",
            },
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())

        # login as normal user
        user_token = self.login("user2@test.com", "pass1234")

        # normal user tries to create a user -> should be 403
        res = self.client.post(
            "/api/v1/users/",
            json={
                "email": "hacker@test.com",
                "password": "pass1234",
            },
            headers=self.auth_headers(user_token),
        )
        self.assertEqual(res.status_code, 403)

    def test_04_places_public_get_and_authenticated_create(self):
        admin_token = self.login("admin@hbnb.io", "admin1234")

        # create normal user
        res = self.client.post(
            "/api/v1/users/",
            json={
                "email": "place_owner@test.com",
                "password": "pass1234",
                "first_name": "Place",
                "last_name": "Owner",
            },
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        owner_id = res.get_json()["id"]
        owner_token = self.login("place_owner@test.com", "pass1234")

        # public get places (should work even if empty)
        res = self.client.get("/api/v1/places/")
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertTrue(isinstance(res.get_json(), list))

        # create place requires jwt
        res = self.client.post(
            "/api/v1/places/",
            json={
                "title": "My Place",
                "description": "Nice",
                "price_per_night": 100.0,
            },
            headers=self.auth_headers(owner_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        place = res.get_json()
        self.assertEqual(place["title"], "My Place")
        self.assertEqual(place["owner_id"], owner_id)
        self.assertIn("id", place)

        # public get place by id
        place_id = place["id"]
        res = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(res.status_code, 200, res.get_json())

    def test_05_places_update_owner_only(self):
        admin_token = self.login("admin@hbnb.io", "admin1234")

        # create two users
        res = self.client.post(
            "/api/v1/users/",
            json={"email": "ownerA@test.com", "password": "pass1234"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        token_a = self.login("ownerA@test.com", "pass1234")

        res = self.client.post(
            "/api/v1/users/",
            json={"email": "ownerB@test.com", "password": "pass1234"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        token_b = self.login("ownerB@test.com", "pass1234")

        # create place by A
        res = self.client.post(
            "/api/v1/places/",
            json={"title": "A Place", "price_per_night": 50.0},
            headers=self.auth_headers(token_a),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        place_id = res.get_json()["id"]

        # B tries to update -> 403
        res = self.client.put(
            f"/api/v1/places/{place_id}",
            json={"title": "Hacked"},
            headers=self.auth_headers(token_b),
        )
        self.assertEqual(res.status_code, 403)

        # A updates -> 200
        res = self.client.put(
            f"/api/v1/places/{place_id}",
            json={"title": "Updated Title"},
            headers=self.auth_headers(token_a),
        )
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(res.get_json()["title"], "Updated Title")

        # admin can update too -> 200
        res = self.client.put(
            f"/api/v1/places/{place_id}",
            json={"title": "Admin Update"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(res.get_json()["title"], "Admin Update")

    def test_06_reviews_rules_and_constraints(self):
        admin_token = self.login("admin@hbnb.io", "admin1234")

        # create owner & reviewer
        res = self.client.post(
            "/api/v1/users/",
            json={"email": "r_owner@test.com", "password": "pass1234"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        owner_id = res.get_json()["id"]
        owner_token = self.login("r_owner@test.com", "pass1234")

        res = self.client.post(
            "/api/v1/users/",
            json={"email": "r_reviewer@test.com", "password": "pass1234"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        reviewer_token = self.login("r_reviewer@test.com", "pass1234")

        # owner creates place
        res = self.client.post(
            "/api/v1/places/",
            json={"title": "Reviewable Place", "price_per_night": 20.0},
            headers=self.auth_headers(owner_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        place_id = res.get_json()["id"]

        # owner tries to review own place -> 403 (حسب الكود عندك في reviews.py)
        res = self.client.post(
            "/api/v1/reviews/",
            json={"text": "I love my place", "rating": 5, "place_id": place_id},
            headers=self.auth_headers(owner_token),
        )
        self.assertIn(res.status_code, (400, 403))  # depending on implementation
        # reviewer creates review -> 201
        res = self.client.post(
            "/api/v1/reviews/",
            json={"text": "Great!", "rating": 5, "place_id": place_id},
            headers=self.auth_headers(reviewer_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        review_id = res.get_json()["id"]

        # reviewer tries duplicate review -> 400
        res = self.client.post(
            "/api/v1/reviews/",
            json={"text": "Again", "rating": 4, "place_id": place_id},
            headers=self.auth_headers(reviewer_token),
        )
        self.assertEqual(res.status_code, 400)

        # update review by same reviewer -> 200
        res = self.client.put(
            f"/api/v1/reviews/{review_id}",
            json={"text": "Updated text", "rating": 4},
            headers=self.auth_headers(reviewer_token),
        )
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(res.get_json()["rating"], 4)

    def test_07_amenities_admin_only_create_update(self):
        admin_token = self.login("admin@hbnb.io", "admin1234")

        # create normal user
        res = self.client.post(
            "/api/v1/users/",
            json={"email": "amen_user@test.com", "password": "pass1234"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        user_token = self.login("amen_user@test.com", "pass1234")

        # normal user tries to create amenity -> should fail
        res = self.client.post(
            "/api/v1/amenities/",
            json={"name": "WiFi"},
            headers=self.auth_headers(user_token),
        )
        # depending on your amenities endpoint, it may be 401/403
        self.assertIn(res.status_code, (401, 403))

        # admin creates amenity
        res = self.client.post(
            "/api/v1/amenities/",
            json={"name": "WiFi"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 201, res.get_json())
        amenity_id = res.get_json()["id"]

        # list amenities public or protected حسب تطبيقك (بعضكم يخلي GET public)
        res = self.client.get("/api/v1/amenities/")
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertTrue(any(a["name"] == "WiFi" for a in res.get_json()))

        # admin updates amenity
        res = self.client.put(
            f"/api/v1/amenities/{amenity_id}",
            json={"name": "Fast WiFi"},
            headers=self.auth_headers(admin_token),
        )
        self.assertEqual(res.status_code, 200, res.get_json())
        self.assertEqual(res.get_json()["name"], "Fast WiFi")


if __name__ == "__main__":
    unittest.main(verbosity=2)
