from fastapi import APIRouter
from auth.models import RegUserModel
from db.db_connection import async_session
import uuid
import datetime
from db.model import User, UserSubscription

auth_router = APIRouter(
    prefix='/reg',
    tags=['Registration']
)

@auth_router.post('/register_user')
async def register_user(request: RegUserModel):
    async with async_session() as session:
        registered_user = User(
            id = uuid.uuid4(),
            name = request.name,
            surname = request.surname,
            email = request.email,
            date_of_registration = datetime.datetime.utcnow(),
        )
        session.add(registered_user)
        await session.commit()
        
    return {'status':'user_registered'}

