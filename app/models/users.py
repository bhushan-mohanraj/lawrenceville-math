from .base import Model, Column, types

from werkzeug.security import generate_password_hash, check_password_hash


class User(Model):
    email = Column(
        types.String(100),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        types.String(1000),
        nullable=False,
    )

    staff = Column(
        types.Boolean,
        default=False,
        nullable=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
