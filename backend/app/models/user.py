from datetime import datetime

from app.db import get_db

# users collection.
# mongodb does not force a fixed structure, so I am keeping the shape here
# so that every user document looks the same.
#
# a user document looks like:
# {
#   "_id": ObjectId,
#   "name": str,
#   "email": str,          -> unique, used for login
#   "password": str,       -> stored as a hash, never the real password
#   "role": str,           -> "user" or "admin"
#   "created_at": datetime
# }


def users():
    return get_db()["users"]


def create_indexes():
    # email must be unique so two people cannot register with same email
    users().create_index("email", unique=True)


def make_user(name, email, password_hash, role="user"):
    # just builds the dict, does not save it. saving + password hashing
    # will be done in the auth sprint.
    return {
        "name": name,
        "email": email,
        "password": password_hash,
        "role": role,
        "created_at": datetime.utcnow(),
    }
