from flask import Blueprint, jsonify

from app.db import get_db

# simple route to check the server is running and can reach mongodb.

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    try:
        get_db().command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = "not connected"

    return jsonify({"status": "ok", "database": db_status})
