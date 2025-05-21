from abc import ABC
from sqlalchemy import select
from db.model import User
from db.db_connection import async_session
from logger import get_logger

logger = get_logger(__name__)

class AbstractUserRepository(ABC):
    """
    async def register_user(self):
        raise NotImplementedError
    """


class UserRepository(AbstractUserRepository):
    def __init__(self, db):
        self.session_factory = db

    async def get_user_by_email(self, email):
        async with self.session_factory() as session:
            async with session.begin():
                query = select(User).where(User.email == email)
                user = await session.execute(query)
                user_obj = user.scalar()
                if user_obj:
                    user_dict = {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'name': user_obj.name,
                        'surname': user_obj.surname,
                        'date_of_registration': user_obj.date_of_registration,
                        'hashed_password': user_obj.hashed_password
                    }
                    logger.debug(f'User info in user_repository:{user_dict}')
                    return user_dict
                return None
            
    async def get_user_by_id(self, user_id):
        async with self.session_factory as session:
            async with session.begin():
                query = (
                    select(User)
                    .where(User.id == user_id)
                )

                user = await session.execute(query)
                return user.scalar()
            
user_repository = UserRepository(async_session)