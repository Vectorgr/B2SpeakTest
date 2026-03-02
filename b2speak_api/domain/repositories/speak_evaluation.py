from abc import ABC, abstractmethod
from ..models.speak_evaluation import SpeakEvaluation, SpeakEvaluationCreate

class SpeakEvaluationRepository(ABC):

    @abstractmethod
    async def create(self, speak_evaluation: SpeakEvaluationCreate) -> SpeakEvaluation:
        pass
    
    @abstractmethod
    async def get(self, id: str) -> SpeakEvaluation:
        pass

    @abstractmethod
    async def findByFileName(self, filename: str) -> SpeakEvaluation:
        pass
    
    @abstractmethod
    async def findByUserId(self, user_id: str) -> list[SpeakEvaluation]:
        pass

    @abstractmethod
    async def update(self, id: str, update_data: dict) -> SpeakEvaluation | None:
        pass

class StorageService(ABC):

    @abstractmethod
    async def upload(self, file_name: str, content: bytes) -> str:
        pass
