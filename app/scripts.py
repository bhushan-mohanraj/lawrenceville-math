from . import models

models.Model.metadata.create_all(bind=models.db_engine)


def create_users():
    user = models.User(email="b@b.com")

    user.set_password("1234")

    models.db_session.add(user)
    models.db_session.commit()
