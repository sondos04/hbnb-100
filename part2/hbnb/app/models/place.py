from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Represents a place in the HBnB application."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        # title (required, max 100)
        if not isinstance(title, str):
            raise TypeError("title must be a string.")
        title = title.strip()
        if not title:
            raise ValueError("title is required.")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters.")

        # description (optional)
        if description is None:
            description = ""
        if not isinstance(description, str):
            raise TypeError("description must be a string.")
        description = description.strip()

        # price (positive float)
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number.")
        if price <= 0:
            raise ValueError("price must be a positive value.")

        # latitude (range -90..90)
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be a number.")
        latitude = float(latitude)
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0.")

        # longitude (range -180..180)
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be a number.")
        longitude = float(longitude)
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0.")

        # owner (User instance)
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance.")

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to this place."""
        from app.models.review import Review  # local import to avoid circular imports

        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance.")
        if getattr(review, "place", None) is not self:
            raise ValueError("review.place must reference this Place.")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        from app.models.amenity import Amenity  # local import to avoid circular imports

        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance.")
        if amenity in self.amenities:
            return  # avoid duplicates
        self.amenities.append(amenity)
        self.save()

    def to_dict(self):
        """Return a dictionary representation of the place."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id,
            "amenity_ids": [a.id for a in self.amenities],
            "review_ids": [r.id for r in self.reviews],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
