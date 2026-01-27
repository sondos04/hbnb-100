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

with app.app_context():
    db.create_all()


if name == "main":
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))
