from app.models.base import *


class User(Model):
    email = Column(
        types.String(100),
        unique=True,
        nullable=False,
    )

    staff = Column(
        types.Boolean,
        default=False,
        nullable=False,
    )

    name = Column(
        types.String(1000),
        nullable=False,
    )
