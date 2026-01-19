from app import create_app
from config import DevelopmentConfig
from app.db.database import get_engine
from app.models.base_model import Base

app = create_app(DevelopmentConfig)

engine = get_engine("development")
Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(debug=True)
