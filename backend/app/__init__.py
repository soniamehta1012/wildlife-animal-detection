from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.db import init_db
from app.models import user, prediction


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # allow the frontend (running on a different domain) to call this api
    CORS(app)

    # connect to mongodb and set up the indexes when the app starts
    init_db(app)
    user.create_indexes()
    prediction.create_indexes()

    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.predictions import predictions_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(predictions_bp, url_prefix="/api/predictions")

    return app
