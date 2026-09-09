import os

# all the settings are kept here so we don't hardcode anything in the code.
# values are read from environment variables (.env file), and if they are
# not set we fall back to some default so it still runs on my laptop.


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # mongodb connection. locally it is just localhost, on Railway we will
    # put the real connection string in the dashboard.
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "wildlife_db")

    # limit image upload size to 16 MB (will be used later in upload api)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
