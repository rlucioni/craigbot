from sqlalchemy import create_engine, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    craigslist_id = Column(Integer, unique=True)

    name = Column(String)
    price = Column(Float)
    link = Column(String, unique=True)
    created = Column(DateTime)

    area = Column(String)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    location = Column(String)
    nearest_stop = Column(String)

    def __repr__(self):
        return f'<Listing(name={self.name}, price={self.price}, craigslist_id={self.craigslist_id})>'


engine = create_engine('sqlite:///apartments.db')
Base.metadata.create_all(engine)
