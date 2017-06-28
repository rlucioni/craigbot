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


engine = create_engine('sqlite:///craigbot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
