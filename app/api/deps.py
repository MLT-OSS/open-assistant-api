from sqlmodel import Session

from app.providers import database


def get_session():
    with Session(database.engine) as session:
        yield session
