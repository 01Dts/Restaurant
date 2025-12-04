from flask import Blueprint, request, jsonify
from auth.auth_service import authenticate_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400

    token = authenticate_user(data["username"], data["password"])
    if not token:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "username": data["username"]
    })
