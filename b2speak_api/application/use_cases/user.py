from b2speak_api.domain.models.user import User, UserCreate
from b2speak_api.domain.repositories.user import UserRepository
from b2speak_api.infrastructure.auth import get_password_hash
from b2speak_api.infrastructure.azure_blob_storage import AzureBlobStorage
from b2speak_api.infrastructure.mongodb_repositories.speak_evaluation import MongoSpeakEvaluationRepository
from b2speak_api.domain.models.speak_evaluation import SpeakEvaluation, SpeakEvaluationCreate
from datetime import datetime
import uuid

class UserUseCase:

    def __init__(self, repository:UserRepository, storage_service: AzureBlobStorage):
        self.repository = repository
        self.storage_service = storage_service

    async def create(self, name: str, email: str, password: str) -> UserCreate:
        hashed_password = get_password_hash(password)
        user_create = UserCreate(
            name=name, 
            email=email, 
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        return await self.repository.create(user_create)

    async def get(self, id : str) -> User:        
        return await self.repository.get(id)
    
    async def get_by_email(self, email : str) -> User | None:
        return await self.repository.get_by_email(email)
    
