from b2speak_api.domain.repositories.speaking_image import SpeakingImageRepository
from b2speak_api.infrastructure.azure_blob_storage import AzureBlobStorage
from b2speak_api.infrastructure.mongodb_repositories.speak_evaluation import MongoSpeakEvaluationRepository
from b2speak_api.domain.models.speak_evaluation import SpeakEvaluation, SpeakEvaluationCreate
from datetime import datetime
import uuid

class UploadSpeakEvaluationUseCase:

    def __init__(self, repository:MongoSpeakEvaluationRepository, storage_service: AzureBlobStorage, speaking_image_repository: SpeakingImageRepository):
        self.repository = repository
        self.storage_service = storage_service
        self.speaking_image_repository = speaking_image_repository # To get the random speaking image

    async def execute(self, content: bytes, selected_picture: str | None = None, user_id: str | None = None) -> SpeakEvaluationCreate:
        filename = f"{uuid.uuid4().hex}.wav"
        file_url = await self.storage_service.upload_audio(filename, content)

        if selected_picture is None:
            get_ramdom_image = await self.speaking_image_repository.get_random()
            if get_ramdom_image is not None:
                selected_picture = get_ramdom_image._id
            if selected_picture is None:
                selected_picture = '0' # Default picture id when no image is available

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
