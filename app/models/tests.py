from datetime import datetime

from sqlalchemy import (
    Column,
    String,
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
