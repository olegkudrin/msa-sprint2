from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base
from .options import config

engine = create_engine(config.database.url, echo=config.database.echo)


def create_tables():
    Base.metadata.create_all(engine)


def get_session():
    return Session(engine)
