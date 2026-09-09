from flask import Blueprint, jsonify

# simple route to check the server is running.
# in the next sprint this will also check the mongodb connection.

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"})
