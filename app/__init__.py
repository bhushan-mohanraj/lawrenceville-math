import os

from flask import Flask


def create_app():
    """Create the application."""

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.urandom(32),
        DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3"),
    )

    with app.app_context():
        from .models import register_models
        from .views import register_views

        register_models(app)
        register_views(app)

    return app
