import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.model import Base, Dataset, Job


engine = create_engine(os.environ["DB_URL"])
Base.metadata.create_all(engine)

def get_session() -> Session:
    return sessionmaker(engine, expire_on_commit=False)