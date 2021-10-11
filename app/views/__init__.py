from flask import render_template, request, redirect

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

    @app.before_request
    def force_https():
        if not request.is_secure:
            url = request.url.replace("http://", "https://", 1)

            return redirect(url)

    @app.route("/")
    def index():
        return render_template("index.html")
