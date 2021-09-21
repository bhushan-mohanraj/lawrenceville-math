from app.helpers import current_edt_datetime
from app.models.base import *

from sqlalchemy.orm import relationship


class Test(Model):
    name = Column(
        types.String(100),
        nullable=False,
    )

    start = Column(
        types.DateTime,
        nullable=False,
    )

    end = Column(
        types.DateTime,
        nullable=False,
    )

    # The choices for the test category.
    TRYOUT = "tryout"
    PRACTICE = "practice"

    category = Column(
        types.Enum(TRYOUT, PRACTICE),
        nullable=False,
    )

    @property
    def active(self) -> bool:
        return self.start <= current_edt_datetime() <= self.end

    @property
    def over(self) -> bool:
        return self.end < current_edt_datetime()


class Problem(Model):
    test_id = Column(
        schema.ForeignKey("Test.id"),
    )

    test = relationship("Test", backref="problems")

    statement = Column(
        types.String(1000),
        nullable=False,
    )

    answer = Column(
        types.Integer,
        nullable=False,
    )


class ProblemAttempt(Model):
    problem_id = Column(
        schema.ForeignKey("Problem.id"),
        nullable=False,
    )

    problem = relationship("Problem", backref="attempts")

    user_id = Column(
        schema.ForeignKey("User.id"),
        nullable=False,
    )

    user = relationship("User", backref="attempts")

    answer = Column(
        types.Integer,
        nullable=False,
    )

    @property
    def correct(self):
        return self.answer == self.problem.answer
