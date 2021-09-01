from .base import (
    Model,
    db_session,
    db_engine,
)

from .users import (
    User,
)

from .events import (
    Event,
)

from .tests import (
    Test,
    # Problem,
    # Attempt,
)


def register_models(app):
    """Register the application models."""

    # Remove the database session after each request ends.
    # See https://docs.sqlalchemy.org/en/14/orm/contextual.html.
    @app.teardown_appcontext
    def remove_db_session(exception=None):
        db_session.remove()
