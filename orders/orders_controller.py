from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from orders.orders_service import fetch_orders

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():
    status = request.args.get("order_status")
    start = request.args.get("start_date")
    end = request.args.get("end_date")

    result = fetch_orders(status, start, end)
    return jsonify(result)
