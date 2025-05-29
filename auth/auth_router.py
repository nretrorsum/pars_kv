from fastapi import APIRouter, Response, Cookie
from auth.models import RegUserModel, LoginUser
from db.db_connection import async_session
import uuid
import datetime
from typing import Optional
import logging
from db.model import User, UserSubscription
from auth.auth_services import login_service, get_current_user, user_dependency
from auth.auth_services import bcrypt_context


#logging.basicConfig(level=logging.DEBUG)

auth_router = APIRouter(
    prefix='/reg',
    tags=['Auth']
)

@auth_router.post('/register_user')
async def register_user(request: RegUserModel):
    async with async_session() as session:
        registered_user = User(
            id = uuid.uuid4(),
            name = request.name,
            surname = request.surname,
            email = request.email,
            hashed_password = bcrypt_context.hash(request.password),
            date_of_registration = datetime.datetime.utcnow(),
        )
        session.add(registered_user)
        await session.commit()
        
    return {'status':'user_registered'}

@auth_router.post('/login', status_code=200)
async def login_user(user_request: LoginUser, response: Response):
    try:
        return await login_service(response=response, user_login=user_request.login, user_password=user_request.password)
    except Exception as e:
        return {'error': e}

@auth_router.post('/me')
async def get_user(authToken: Optional[str] = Cookie(alias='authToken', default=None)):
    try:
        user = await get_current_user(token = authToken)
        logging.info(f'User info in /me endpoint:{user}')
        return user
    except Exception as e:      
        return {'error': str(e)}
    
@auth_router.post('/test_me')
async def get_user(current_user: user_dependency):
    try:
        return current_user
    except Exception as e:      
        return {'error': str(e)}

@auth_router.post('/logout',status_code = 204)
async def logout(response: Response, authToken: Optional[str] = Cookie(alias='authToken', default=None)):
    response.set_cookie(
        key='authToken',
            value='',
            max_age=0,
            secure=False,
            httponly=False,
            samesite='lax'
    )
    return {'status':'User log out'}