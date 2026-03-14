from fileinput import filename

from b2speak_api.infrastructure.azure_blob_storage import AzureBlobStorage
from b2speak_api.domain.models.speaking_image import SpeakingImage, SpeakingImageCreate
from b2speak_api.infrastructure.mongodb_repositories.speaking_image import MongoSpeakingImageRepository
from datetime import datetime
import uuid


class SpeakingImageUseCase:

    def __init__(self, repository:MongoSpeakingImageRepository, storage_service: AzureBlobStorage):
        self.repository = repository
        self.storage_service = storage_service

    async def add(self, content: bytes, user_id: str | None = None) -> SpeakingImageCreate:
        filename = f"{uuid.uuid4().hex}.jpg"
        file_url = await self.storage_service.upload_speaking_image(filename, content)

        document = SpeakingImageCreate(
            image_url=file_url,
            filename=filename,
            user_id=user_id,
            created_at=datetime.utcnow()
        )

        return await self.repository.add(document)
    
    async def get_random(self) -> SpeakingImage | None: 
        print("Getting random speaking image")       
        return await self.repository.get_random()
    
    async def get(self, id : str) -> SpeakingImage | None:        
        return await self.repository.get(id)
    
    async def download_image(self, id: str) -> bytes:
        image = await self.repository.get(id)
        if image is None:
            return b""
        return await self.storage_service.download_speaking_image(image.filename)
    