from sqlalchemy import create_engine, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


Base = declarative_base()


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, server_default=func.now())
    craigslist_id = Column(String, unique=True)
    url = Column(String, unique=True)


# This directory is created by the Dockerfile. A corresponding data volume is
# mounted at container run time.
engine = create_engine('sqlite:////var/db/craigbot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
