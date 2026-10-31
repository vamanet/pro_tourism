import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "tourism.db"),
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-to-a-long-random-string")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(BASE_DIR), "static", "images")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
