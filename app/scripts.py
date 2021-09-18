from datetime import datetime

from app import models


def create_db():
    models.Model.metadata.create_all(bind=models.db_engine)


def create_events():
    event = models.Event(
        name="Event",
        start=datetime(2021, 1, 1),
        end=datetime(2021, 1, 2),
        category=models.Event.MEETING,
    )

    models.db_session.add(event)
    models.db_session.commit()


def create_tests():
    test = models.Test(
        name="Test",
        start=datetime(2021, 1, 1),
        end=datetime(2021, 1, 2),
        category=models.Test.TRYOUT,
    )

    models.db_session.add(test)
    models.db_session.commit()

    problem = models.Problem(
        test_id=test.id,
        statement="What is 1 + 1?",
        answer=2,
    )

    models.db_session.add(problem)
    models.db_session.commit()
