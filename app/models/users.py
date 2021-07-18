from sqlalchemy import (
    Column,
    String,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from .base import Model


class User(Model):
    username = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String(1000),
        nullable=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
