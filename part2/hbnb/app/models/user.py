from app.models.base_model import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        # first_name (required, max 50)
        if not isinstance(first_name, str):
            raise TypeError("first_name must be a string.")
        first_name = first_name.strip()
        if not first_name:
            raise ValueError("first_name is required.")
        if len(first_name) > 50:
            raise ValueError("first_name must be at most 50 characters.")

        # last_name (required, max 50)
        if not isinstance(last_name, str):
            raise TypeError("last_name must be a string.")
        last_name = last_name.strip()
        if not last_name:
            raise ValueError("last_name is required.")
        if len(last_name) > 50:
            raise ValueError("last_name must be at most 50 characters.")

        # email (required, valid format)
        if not isinstance(email, str):
            raise TypeError("email must be a string.")
        email = email.strip().lower()
        if not email:
            raise ValueError("email is required.")

        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValueError("email format is invalid.")

        # is_admin (boolean)
        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be a boolean.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
