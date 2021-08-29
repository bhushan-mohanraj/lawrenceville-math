from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
)

from .base import Model


class Event(Model):
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

    # The choices for the event category.
    MEETING = "meeting"
    CONTEST = "contest"

    category = Column(
        Enum(MEETING, CONTEST),
        nullable=False,
    )

    link = Column(
        String(1000),
    )
