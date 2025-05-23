from pydantic import BaseModel
from datetime import datetime
import uuid
from decimal import Decimal
from typing import Optional

class UserRegistrationModel(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: str
    date_of_registration: datetime

    class Config:
        from_attributes = True


class RegUserModel(BaseModel):
    name: str
    surname: str
    password: str
    email: str

class UserModelResponse(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: str
    date_of_registration: datetime
    subscription: Optional['UserSubscriptionModel']  # Це буде заміщене на модель UserSubscriptionModel

    class Config:
        from_attributes = True


class UserSubscriptionModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    subscription_id: uuid.UUID
    start_date: datetime
    end_date: datetime
    status: str

    class Config:
        from_attributes = True


class SubscriptionModel(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    price: Decimal
    duration_days: int

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    login: str
    password: str