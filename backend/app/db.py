from pymongo import MongoClient

# we make one mongo client for the whole app and reuse it.
# making a new connection on every request would be slow.

client = None
db = None


def init_db(app):
    global client, db
    client = MongoClient(app.config["MONGO_URI"])
    db = client[app.config["DB_NAME"]]
    print("Connected to MongoDB ->", app.config["DB_NAME"])
    return db


def get_db():
    return db
