from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_all():
    user = User("John", "Doe", "john@example.com")
    print("User OK")

    place = Place("Beach House", "Nice view", 250.0, 24.5, 46.7, user)
    print("Place OK")

    review = Review("Amazing place", 5, place, user)
    print(" Review OK")

    amenity = Amenity("Wi-Fi")
    print("Amenity OK")

    place.add_review(review)
    place.add_amenity(amenity)

    assert place.reviews[0].text == "Amazing place"
    assert place.amenities[0].name == "Wi-Fi"
    print(" Relationships OK")

test_all()
