from flask import Flask, jsonify
from config import Config
from jwt_extensions import init_jwt
from auth.auth_controller import auth_bp
from orders.orders_controller import orders_bp
from menu.menu_controller import menu_bp
from error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_jwt(app)  # Initialize JWT

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(menu_bp)

    register_error_handlers(app)

    @app.route("/")
    def home():
        return jsonify({"status": "ok", "message": "Restaurant API Running"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
