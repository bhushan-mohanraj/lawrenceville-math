from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
)

from sqlalchemy.orm import relationship

from .base import Model


class Test(Model):
    """
    A math club test, such as a tryout or practice test.
    """

    name = Column(
        String(100),
        nullable=False,
    )

    # The start and end of the test window.
    start = Column(
        DateTime,
    )

    end = Column(
        DateTime,
    )

    time_limit = Column(
        Boolean,
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
