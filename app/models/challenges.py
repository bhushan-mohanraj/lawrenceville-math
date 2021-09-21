from app.helpers import current_edt_datetime
from app.models.base import *

from sqlalchemy.orm import relationship


class Challenge(Model):
    statement = Column(
        types.String(1000),
        nullable=False,
    )

    answer = Column(
        types.Integer,
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

    @property
    def active(self) -> bool:
        return self.start <= current_edt_datetime() <= self.end

    @property
    def over(self) -> bool:
        return self.end < current_edt_datetime()


class ChallengeAttempt(Model):
    challenge_id = Column(
        schema.ForeignKey("Challenge.id"),
        nullable=False,
    )

    challenge = relationship(
        "Challenge",
        backref="attempts",
    )

    user_id = Column(
        schema.ForeignKey("User.id"),
        nullable=False,
    )

    user = relationship("User")

    answer = Column(
        types.Integer,
        nullable=False,
    )

    @property
    def correct(self):
        return self.answer == self.challenge.answer
