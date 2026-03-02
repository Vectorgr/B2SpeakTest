from abc import ABC, abstractmethod
from ..models.user import UserCreate, User

class UserRepository(ABC):

    @abstractmethod
    async def create(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def get(self, id: str) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def update(self, id: str, update_data: dict) -> User | None:
        pass

