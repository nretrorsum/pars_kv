from sqlalchemy import (Integer, String, TIMESTAMP, Column, 
                        ForeignKey, Boolean, DECIMAL, UUID, 
                        JSON, Float, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

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
    hashed_password = Column(String)
    email = Column(String, nullable=False)
    date_of_registration = Column(TIMESTAMP, nullable=False)
    
    subscription = relationship("UserSubscription", back_populates="user", uselist=False)
    apartments = relationship("Apartment", back_populates="seller", cascade="all, delete-orphan")

class Rieltors(Base):
    __tablename__ = "rieltors"

    id = Column(UUID(as_uuid = True),primary_key = True, default = uuid.uuid4, unique = True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, nullable = False)
    date_of_registration = Column(TIMESTAMP, nullable = False)

class BannedIP(Base):
    __tablename__ = "banned_ip"

    id = Column(UUID(as_uuid = True),primary_key = True, default = uuid.uuid4, unique = True)
    ip = Column(String, nullable = False)
    date_of_ban = Column(TIMESTAMP, nullable = False)

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
    
class ExpiredAccessTokens(Base):
    __tablename__ = 'expired_tokens'
    
    id = Column(UUID(as_uuid=True),primary_key=True, unique=True, nullable=False, default = uuid.uuid4)
    token = Column(String, nullable=False)
    
class Subscription(Base):
    __tablename__ = 'subscription'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(length=100), nullable=False)
    description = Column(String)
    price = Column(DECIMAL, nullable=False)
    duration_days = Column(Integer, nullable=False)
    
    # Зв'язок з таблицею user_subscription
    user_subscriptions = relationship("UserSubscription", back_populates="subscription")

class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(UUID(as_uuid = True),primary_key = True, default = uuid.uuid4, unique = True)
    title = Column(String, nullable=False)  # Заголовок оголошення
    description = Column(Text, nullable=True)
    
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")  # або UAH, EUR

    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)

    rooms = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    area = Column(Float, nullable=False)  # Загальна площа
    living_area = Column(Float, nullable=True)
    kitchen_area = Column(Float, nullable=True)

    year_built = Column(Integer, nullable=True)
    building_type = Column(String, nullable=True)  # Наприклад: "Panel", "Brick", "Monolith"
    condition = Column(String, nullable=True)  # "New", "Needs renovation", etc.

    has_balcony = Column(Boolean, default=False)
    is_furnished = Column(Boolean, default=False)

    listed_date = Column(TIMESTAMP, default=False)
    is_active = Column(Boolean, default=True)

    seller_id = Column(UUID, ForeignKey("users.id"))  # Продавець (агент / власник)
    seller = relationship("User", back_populates="apartments")

