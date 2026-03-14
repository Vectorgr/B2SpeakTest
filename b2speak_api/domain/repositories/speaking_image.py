from abc import ABC, abstractmethod

from b2speak_api.domain.models.speaking_image import SpeakingImage, SpeakingImageCreate
from ..models.speaking_image import SpeakingImage, SpeakingImageCreate

class SpeakingImageRepository(ABC):

    @abstractmethod
    async def add(self, speaking_image: SpeakingImageCreate) -> SpeakingImage:
        pass
    
    @abstractmethod
    async def get(self, id: str) -> SpeakingImage | None:
        pass

    @abstractmethod
    async def get_random(self) -> SpeakingImage | None:
        pass



class StorageService(ABC):

    @abstractmethod
    async def upload(self, file_name: str, content: bytes) -> str:
        pass
