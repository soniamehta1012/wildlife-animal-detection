from flask import Blueprint, jsonify

# auth routes - only stubs for now.
# the actual register/login will be done in the Optimization & Security sprint.
# keeping these here so the api structure is ready and frontend knows the urls.

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    return jsonify({"message": "register not implemented yet"}), 501


@auth_bp.post("/login")
def login():
    return jsonify({"message": "login not implemented yet"}), 501
