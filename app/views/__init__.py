from . import (
    main,
    users,
    events,
)


def register_views(app):
    """Register the application views."""

    blueprints = [
        main.bp,
        users.bp,
        events.bp,
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
