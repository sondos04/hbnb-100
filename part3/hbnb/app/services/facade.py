from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.amenity_repository import AmenityRepository


class HBnBFacade:
    def init(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ======================
    # Users
    # ======================
    def create_user(self, email, password, first_name=None, last_name=None, is_admin=False):
        if not email or not password:
            raise ValueError("Email and password are required")

        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already exists")

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=bool(is_admin),
        )
        user.set_password(password)

        return self.user_repo.add(user)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_id(self, user_id):
        return self.user_repo.get_by_id(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def update_user(self, user, data, is_admin=False):
        # user: object already fetched
        # regular user: only first_name/last_name
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        if is_admin:
            if "email" in data:
                # ensure unique email
                existing = self.user_repo.get_by_email(data["email"])
                if existing and existing.id != user.id:
                    raise ValueError("Email already exists")
                user.email = data["email"]

            if "password" in data and data["password"]:
                user.set_password(data["password"])

        db.session.commit()
        return user

    # ======================
    # Places
    # ======================
    def create_place(self, owner_id, title, description="", price_per_night=0.0):
        if not title:
            raise ValueError("Title is required")

        owner = self.user_repo.get_by_id(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=title,
            description=description or "",
            price_per_night=float(price_per_night or 0.0),
            owner_id=owner_id,
        )
        return self.place_repo.add(place)

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place_by_id(self, place_id):
        return self.place_repo.get_by_id(place_id)

    def update_place(self, place, data):
        if "title" in data and data["title"]:
            place.title = data["title"]
        if "description" in data:
            place.description = data.get("description") or ""
        if "price_per_night" in data:
            place.price_per_night = float(data.get("price_per_night") or 0.0)

        db.session.commit()
        return place

    def delete_place(self, place):
        return self.place_repo.delete(place)

    # ======================
    # Reviews
    # ======================
    def create_review(self, user_id, place_id, text, rating):
        if not text:
            raise ValueError("Review text is required")

        if rating is None or not (1 <= int(rating) <= 5):
            raise ValueError("Rating must be between 1 and 5")

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found")

        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")

        existing = self.review_repo.get_by_user_and_place(user_id, place_id)
        if existing:
            raise ValueError("You have already reviewed this place")

        review = Review(
            text=text,
            rating=int(rating),
            user_id=user_id,
            place_id=place_id,
        )
        return self.review_repo.add(review)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_review_by_id(self, review_id):
        return self.review_repo.get_by_id(review_id)

    def update_review(self, review, data):
        if "text" in data and data["text"]:
            review.text = data["text"]

        if "rating" in data and data["rating"] is not None:
            r = int(data["rating"])
            if not (1 <= r <= 5):
                raise ValueError("Rating must be between 1 and 5")
            review.rating = r

        db.session.commit()
        return review

    def delete_review(self, review):
        return self.review_repo.delete(review)

    # ======================
    # Amenities
    # ======================
    def create_amenity(self, name):
        if not name:
            raise ValueError("Amenity name is required")

        existing = self.amenity_repo.get_by_name(name)
        if existing:
            raise ValueError("Amenity already exists")

        amenity = Amenity(name=name)
        return self.amenity_repo.add(amenity)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity_by_id(self, amenity_id):
        return self.amenity_repo.get_by_id(amenity_id)

    def update_amenity(self, amenity, data):
        if "name" in data and data["name"]:
            # unique check
            existing = self.amenity_repo.get_by_name(data["name"])
            if existing and existing.id != amenity.id:
                raise ValueError("Amenity already exists")
            amenity.name = data["name"]

        db.session.commit()
        return amenity


facade = HBnBFacade()
