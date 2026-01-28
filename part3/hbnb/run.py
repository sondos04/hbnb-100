import os
from app import create_app
from config import DevelopmentConfig, ProductionConfig
from app.extensions import db


def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig


app = create_app(get_config())

# لازم يكون داخل app_context
with app.app_context():
    # مهم: استيراد المودلز قبل create_all
    from app.models.user import User  # noqa: F401
    from app.models.place import Place  # noqa: F401
    from app.models.review import Review  # noqa: F401
    from app.models.amenity import Amenity  # noqa: F401

    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=app.config.get("DEBUG", False)
    )
