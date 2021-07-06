import os

from flask import Flask


def create_app():
    """Create the application."""

    app = Flask(__name__)

    # Configure the app from environment variables, with default values otherwise.
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "development"),
        DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3"),
    )

    return app
