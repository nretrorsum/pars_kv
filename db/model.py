from sqlalchemy import Integer, String, TIMESTAMP, Column, ForeignKey, Boolean, DECIMAL, UUID, JSON
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

class FlatsFromRieltor(Base):
    __tablename__ = 'Flats_from_rieltor'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    price = Column(Integer)
    price_per_m2 = Column(Integer)
    adress = Column(String)
    region = Column(String)
    rooms = Column(Integer)
    total_size = Column(String)
    floor = Column(String)
    description = Column(String)
    link = Column(String)
    photos = Column(JSON)
    date_of_scrap = Column(TIMESTAMP)
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(length=30), nullable=False)
    surname = Column(String)
    email = Column(String, nullable=False)
    date_of_registration = Column(TIMESTAMP, nullable=False)
    
    subscription = relationship("UserSubscription", back_populates="user", uselist=False)
    
class UserSubscription(Base):
    __tablename__ = 'user_subscription'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # зв'язок з таблицею users
    subscription_id = Column(UUID(as_uuid=True), ForeignKey('subscription.id'), nullable=False)  # зв'язок з таблицею subscription
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    status = Column(String, nullable=False)
    
    # Зв'язок з користувачем
    user = relationship("User", back_populates="subscription")
    
    # Зв'язок з підпискою
    subscription = relationship("Subscription", back_populates="user_subscriptions")
    
    
class Subscription(Base):
    __tablename__ = 'subscription'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(length=100), nullable=False)
    description = Column(String)
    price = Column(DECIMAL, nullable=False)
    duration_days = Column(Integer, nullable=False)
    
    # Зв'язок з таблицею user_subscription
    user_subscriptions = relationship("UserSubscription", back_populates="subscription")
    
    