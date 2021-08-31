from sqlalchemy import (
    create_engine,
    Column,
    Integer,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    declarative_base,
    declared_attr,
)

from flask import current_app

db_engine = create_engine(current_app.config["DATABASE_URL"], future=True)
db_session = scoped_session(sessionmaker(bind=db_engine))


class Model:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    id = Column(Integer, primary_key=True)


Model = declarative_base(cls=Model)
