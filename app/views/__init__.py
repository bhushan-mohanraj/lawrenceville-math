from . import main


def register_views(app):
    """Register the application views."""

    app.register_blueprint(main.bp)
