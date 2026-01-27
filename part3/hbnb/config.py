import os

class Config:
    SECRET_KEY = "super-secret-key"
    JWT_SECRET_KEY = "jwt-super-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
