from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, owner, title, price, latitude, longitude, description="", amenities=None):
        super().__init__()

        # title
        if not isinstance(title, str):
            raise TypeError("title must be a string.")
        title = title.strip()
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be less than 100 characters.")

        # owner (User instance)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance.")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner              # User object
        self.owner_id = owner.id
        self.reviews = []
        self.amenities = amenities if amenities else []

    # ===== price =====
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value <= 0:
            raise ValueError("Price must be a positive value.")
        self._price = float(value)

    # ===== latitude =====
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        self._latitude = float(value)

    # ===== longitude =====
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        self._longitude = float(value)

    # ===== relationships =====
    def add_review(self, review):
        from app.models.review import Review

        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance.")
        if review.place is not self:
            raise ValueError("Review must be associated with this Place.")

        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity):
        from app.models.amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance.")

        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.id,
            "reviews": [r.id for r in self.reviews],
            "amenities": [a.id for a in self.amenities],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
