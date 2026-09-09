from flask import Flask

from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # NOTE: connecting to mongodb and creating the indexes is done in the
    # next sprint (Backend setup). in this sprint we are only setting up the
    # architecture, so here we just build the app and register the routes.
    #
    # from app.db import init_db
    # from app.models import user, prediction
    # init_db(app)
    # user.create_indexes()
    # prediction.create_indexes()

    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.predictions import predictions_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(predictions_bp, url_prefix="/api/predictions")

    return app
