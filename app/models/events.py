from .base import Model, Column, types


class Event(Model):
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

    # The choices for the event category.
    MEETING = "meeting"
    CONTEST = "contest"

    category = Column(
        types.Enum(MEETING, CONTEST),
        nullable=False,
    )

    link = Column(
        types.String(1000),
    )
