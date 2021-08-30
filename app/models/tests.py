from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import relationship

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
    def over(self) -> bool:
        """
        Whether the test is over.
        """

    @property
    def length(self) -> int:
        """
        The length of the test in minutes.
        """


class Problem(Model):
    test_id = Column(
        ForeignKey("test.id"),
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
        ForeignKey("problem.id"),
        nullable=False,
    )

    problem = relationship(Problem, backref="attempts")

    user_id = Column(
        ForeignKey("user.id"),
        nullable=False,
    )

    answer = Column(
        Integer,
        nullable=False,
    )

    @property
    def correct(self):
        return self.answer == self.problem.answer