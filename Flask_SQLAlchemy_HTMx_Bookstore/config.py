# config.py

import os

persistent_path = os.getenv("PERSISTENT_STORAGE_DIR", os.path.dirname(os.path.realpath(__file__)))
db_path = os.path.join(persistent_path, "database.db")

SECRET_KEY = "Learn a little here, and a litle there."
SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
