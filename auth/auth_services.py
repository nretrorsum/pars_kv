from db.user_repository import user_repository
from auth.models import UserModelResponse
from fastapi import HTTPException, Cookie, Depends
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError, ExpiredSignatureError
from config import SECRET
from typing import Optional, Annotated
from fastapi import Response, HTTPException
from logger import get_logger

logger = get_logger(__name__)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


async def validate_user_credentials(login: str, password: str):
    try:
        db_user = await user_repository.get_user_by_email(email=login)
        logger.debug(f'User from db in validate_user_credentials:{db_user}')
        if not db_user:
            raise HTTPException(status_code=401, detail='Not authenticated')
        if not bcrypt_context.verify(password, db_user.get('hashed_password')):
            raise HTTPException(status_code=401, detail='Not authenticated')
        return db_user
    except Exception as e:
        logger.debug(f'Excepion in validate_user_credentials:{str(e)}')
        raise HTTPException(status_code=401, detail='Not authenticated')

async def generate_jwt(id: str, 
                       login: str, 
                       name: str, 
                       surname: str,
                       date_of_registration: str, 
                       expiration: timedelta):
    encode = {'id': id, 
              'login':login, 
              'name':name, 
              'surname': surname,
              'date_of_registration': date_of_registration}
    expires = datetime.utcnow()+expiration
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET, 'HS256')

async def validate_jwt_token(token) -> bool:
    """
    token_from_db = await repository.get_expired_token(token)
    if token_from_db:
        return False
    """
    try:
        payload = jwt.decode(token, SECRET, 'HS256')
        expiration_date = payload.get('exp')
        if expiration_date is None:
            return False
        """
        if datetime.utcnow().timestamp() > expiration_date:
            await repository.add_expired_token(token, expired=expiration_date)
            logging.info('expired token added to db')
            return False
        """
        return True
    except:
        return False
    
async def get_current_user(token = Cookie(alias='authToken', default=None)):
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    if await validate_jwt_token(token) == False:
        raise HTTPException(status_code=401, detail='Not authenticated')
    #token_from_db = await repository.get_expired_token(authToken)
    try:
        user_credentials = jwt.decode(token, SECRET, 'HS256')
        return user_credentials
    except JWTError as e:
        return {'status':'Error in token processing', 'error':e}
    
async def login_service(response: Response, user_login: str, user_password: str):
    try:
        logger.debug(f'User credentials:{user_login}')
        user = await validate_user_credentials(login=user_login, password=user_password)
        logger.debug(f'User after validation{user}')
        if user:
            token = await generate_jwt(
            id=str(user['id']), 
            login=user['email'],
            name=user['name'],
            surname=user['surname'],
            date_of_registration=user['date_of_registration'].isoformat(),
            expiration=timedelta(minutes=30)
        )
            logger.debug(f'Auth token:{token}')
        response.set_cookie(
            key='authToken',
            value=token,
            max_age=1800,
            secure=False,
            httponly=False,
            samesite='lax'
        )
        return {'status':'authenticated'}
    except Exception as e:
        logger.debug(f'Excepion in login service:{str(e)}')
        raise HTTPException(status_code=401, detail='Not authenticated')
    
user_dependency = Annotated[dict, Depends(get_current_user)]