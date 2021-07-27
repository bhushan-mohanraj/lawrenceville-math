from . import (
    main,
    users,
)


def register_views(app):
    """Register the application views."""

    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)
