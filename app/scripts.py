from datetime import datetime

from . import models


def create_db():
    models.Model.metadata.create_all(bind=models.db_engine)


def create_users():
    user = models.User(email="staff@staff.com")

    user.staff = True

    user.set_password("staff")

    models.db_session.add(user)
    models.db_session.commit()

    user = models.User(email="user@user.com")

    user.set_password("user")

    models.db_session.add(user)
    models.db_session.commit()


def create_events():
    event = models.Event(
        name="Event",
        start=datetime(2021, 1, 1),
        end=datetime(2021, 1, 3),
    )

    event.category = event.Category.meeting

    models.db_session.add(event)
    models.db_session.commit()
