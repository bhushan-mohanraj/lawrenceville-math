from flask import render_template

from app.views import (
    users,
    events,
    tests,
)


def register_views(app):
    """Register the application views."""

    blueprints = [
        users.bp,
        events.bp,
        tests.bp,
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.route("/")
    def index():
        return render_template("index.html")
