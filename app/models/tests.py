from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import relationship

from ..helpers import current_edt_datetime

from .base import Model


class Test(Model):
    name = Column(
        String(100),
        nullable=False,
    )

    start = Column(
        DateTime,
        nullable=False,
    )

    end = Column(
        DateTime,
        nullable=False,
    )

    # The choices for the test category.
    TRYOUT = "tryout"
    PRACTICE = "practice"

    CATEGORY_CHOICES = [TRYOUT, PRACTICE]

    category = Column(
        Enum(*CATEGORY_CHOICES),
        nullable=False,
    )

    @property
    def active(self) -> bool:
        return self.start <= current_edt_datetime() <= self.end


class Problem(Model):
    test_id = Column(
        ForeignKey("Test.id"),
    )

    test = relationship(Test, backref="problems")

    statement = Column(
        String(1000),
        nullable=False,
    )

    answer = Column(
        Integer,
        nullable=False,
    )


class Attempt(Model):
    problem_id = Column(
        ForeignKey("Problem.id"),
        nullable=False,
    )

    problem = relationship(Problem, backref="attempts")

    user_id = Column(
        ForeignKey("User.id"),
        nullable=False,
    )

    answer = Column(
        Integer,
        nullable=False,
    )

    @property
    def correct(self):
        return self.answer == self.problem.answer
