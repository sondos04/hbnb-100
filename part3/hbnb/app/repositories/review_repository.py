from app.extensions import db
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_by_user_and_place(self, user_id, place_id):
        return (
            self.model.query
            .filter_by(user_id=user_id, place_id=place_id)
            .first()
        )
