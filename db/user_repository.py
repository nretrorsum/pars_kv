from abc import ABC

class AbstractUserRepository(ABC):
    async def register_user(self):
        raise NotImplementedError
    
class UserRepository(AbstractUserRepository):
    def __init__(self, db):
        self.db = db