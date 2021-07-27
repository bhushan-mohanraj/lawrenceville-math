from sqlalchemy import (
    Column,
    String,
    Boolean,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from .base import Model


class User(Model):
    email = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String(1000),
        nullable=False,
    )

    staff = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
