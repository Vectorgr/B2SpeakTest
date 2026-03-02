from b2speak_api.infrastructure.azure_blob_storage import AzureBlobStorage
from b2speak_api.infrastructure.mongodb_repositories.speak_evaluation import MongoSpeakEvaluationRepository
from b2speak_api.domain.models.speak_evaluation import SpeakEvaluation, SpeakEvaluationCreate
from datetime import datetime
import uuid

class UploadSpeakEvaluationUseCase:

    def __init__(self, repository:MongoSpeakEvaluationRepository, storage_service: AzureBlobStorage):
        self.repository = repository
        self.storage_service = storage_service

    async def execute(self, content: bytes, selected_picture: str = '0', user_id: str | None = None) -> SpeakEvaluationCreate:
        filename = f"{uuid.uuid4().hex}.wav"
        file_url = await self.storage_service.upload(filename, content)

        document = SpeakEvaluationCreate(
            selected_picture=selected_picture,
            audio_name = filename,
            audio_url=file_url,
            user_id=user_id,
            state='UPLOADING',
            created_at=datetime.utcnow()
        )

        return await self.repository.create(document)
    
    async def get(self, id : str) -> SpeakEvaluation:        
        return await self.repository.get(id)
    
    async def getByFileName(self, filename : str) -> SpeakEvaluation | None:
        return await self.repository.findByFileName(filename)
    
    async def getByFileName(self, filename : str) -> SpeakEvaluation | None:
        return await self.repository.findByFileName(filename)

    async def getByUserId(self, user_id: str) -> list[SpeakEvaluation]:
        return await self.repository.findByUserId(user_id)
