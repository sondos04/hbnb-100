from app.models.base_model import BaseModel, Base
from app.models.validation import Validator, ValidationError

class Review(BaseModel):
    def __init__(self, text, user_id, place_id, rating=0):
        super().__init__()
        
        # Validate inputs
        self.text = Validator.validate_string(text, "Review text", min_length=1, max_length=1000)
        self.user_id = Validator.validate_uuid(user_id, "User ID")
        self.place_id = Validator.validate_uuid(place_id, "Place ID")
        self.rating = Validator.validate_rating(rating)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "text": self.text,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating
        })
        return data
