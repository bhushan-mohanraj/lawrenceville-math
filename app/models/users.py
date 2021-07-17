from sqlalchemy import (
    Column,
    String,
)

from .base import Model


class User(Model):
    username = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    password = Column(
        String(100),
        nullable=False,
    )
