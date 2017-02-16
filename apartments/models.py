from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    craigslist_id = Column(String, unique=True)
    url = Column(String, unique=True)


engine = create_engine('sqlite:///apartments.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
