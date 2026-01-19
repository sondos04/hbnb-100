from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
	def __init__(self, session):
		super().__init__(session, Place)
	def get_by_owner(self, user_id):
		return(
		self.session.query(Place)
		.filter(Place.owner_id == user_id)
		.all()
		)
