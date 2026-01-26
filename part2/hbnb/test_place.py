#!/usr/bin/env python3
import unittest

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.owner = User(first_name="Owner", last_name="One", email="owner@hbnb.com")

    def test_create_valid_place(self):
        p = Place(
            owner=self.owner,
            title="Nice place",
            price=100,
            latitude=24.7,
            longitude=46.7,
            description="Desc"
        )
        self.assertEqual(p.title, "Nice place")
        self.assertEqual(p.owner.id, self.owner.id)
        self.assertEqual(p.owner_id, self.owner.id)
        self.assertIsInstance(p.reviews, list)
        self.assertIsInstance(p.amenities, list)

    def test_invalid_title_should_fail(self):
        with self.assertRaises(Exception):
            Place(owner=self.owner, title="", price=10, latitude=0, longitude=0)

    def test_invalid_owner_should_fail(self):
        with self.assertRaises(Exception):
            Place(owner=None, title="X", price=10, latitude=0, longitude=0)

    def test_invalid_price_should_fail(self):
        with self.assertRaises(Exception):
            Place(owner=self.owner, title="X", price=-1, latitude=0, longitude=0)

    def test_invalid_latitude_should_fail(self):
        with self.assertRaises(Exception):
            Place(owner=self.owner, title="X", price=10, latitude=100, longitude=0)

    def test_invalid_longitude_should_fail(self):
        with self.assertRaises(Exception):
            Place(owner=self.owner, title="X", price=10, latitude=0, longitude=200)

    def test_add_amenity_and_review(self):
        p = Place(owner=self.owner, title="X", price=10, latitude=0, longitude=0)

        a = Amenity(name="Pool")
        r = Review(text="Good", rating=5, place=p, user=self.owner)

        p.add_amenity(a)
        p.add_review(r)

        self.assertEqual(len(p.amenities), 1)
        self.assertEqual(len(p.reviews), 1)
        self.assertEqual(p.amenities[0].name, "Pool")
        self.assertEqual(p.reviews[0].text, "Good")


if __name__ == "__main__":
    unittest.main(verbosity=2)
