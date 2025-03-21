from sqlalchemy import Integer, String, TIMESTAMP, Column, ForeignKey, Boolean, DECIMAL, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class Flats(Base):
    __tablename__ = 'Flats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    price = Column(Integer, nullable=False)
    price_per_sqm = Column(Integer, nullable=False)
    district = Column(String, nullable=False)
    rooms = Column(String, nullable=False)
    floor = Column(String, nullable=False)
    square = Column(Integer, nullable=False)
    room_squares = Column(String, nullable=False)
    year = Column(String)
    date_of_scrap = Column(TIMESTAMP)
    