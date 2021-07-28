from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum,
)

import enum

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

    class CategoryEnum(enum.Enum):
        meeting = 1
        contest = 2

    category = Column(
        Enum(CategoryEnum),
        nullable=False,
    )

    link = Column(
        String(1000),
    )
