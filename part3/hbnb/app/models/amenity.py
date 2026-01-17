from app.models.base_model import BaseModel, Base


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not isinstance(name, str):
            raise TypeError("name must be a string.")

        name = name.strip()
        if not name:
            raise ValueError("amenity name is required.")

        if len(name) > 50:
            raise ValueError("amenity name must be at most 50 characters.")

        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
