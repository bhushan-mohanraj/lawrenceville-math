from app.models.base import *


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
        doc="A link to details about the event, including the 'https://'.",
    )
