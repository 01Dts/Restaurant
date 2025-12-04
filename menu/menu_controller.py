from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from menu.menu_service import fetch_menu

menu_bp = Blueprint("menu", __name__, url_prefix="/api/menu")

@menu_bp.route("/", methods=["GET"])
@jwt_required()
def menu():
    category = request.args.get("category")
    items = fetch_menu(category)
    return jsonify(items)
