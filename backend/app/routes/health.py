from flask import Blueprint, jsonify

from app.db import get_db

health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def index():
    # simple landing response so the base url shows something useful
    return jsonify({
        "service": "Wildlife Animal Detection API",
        "status": "running",
        "endpoints": ["/health", "/api/auth", "/api/predictions"],
    })


@health_bp.get("/health")
def health():
    # check the server is running and can reach mongodb
    try:
        get_db().command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = "not connected"

    return jsonify({"status": "ok", "database": db_status})
