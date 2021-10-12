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

    house = Column(
        types.Enum(
            # Lower
            "thomas",
            "davidson",
            "perry ross",
            "cromwell",
            # Circle
            "cleve",
            "griswold",
            "woodhull",
            "dickinson",
            "kennedy",
            "hamill",
            # Crescent
            "kirby",
            "carter",
            "stephens",
            "stanley",
            "mcClellan",
            # Upper
            "upper",
            "reynolds",
            "mcPherson",
            "kinnan",
        ),
    )
