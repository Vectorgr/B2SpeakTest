import os
from dotenv import load_dotenv
from b2speak_api.application.use_cases.speaking_image import SpeakingImageUseCase
from b2speak_api.infrastructure.mongodb_repositories.speaking_image import MongoSpeakingImageRepository
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from b2speak_api.application.use_cases.user import UserUseCase
from b2speak_api.infrastructure.mongodb_repositories.speak_evaluation import MongoSpeakEvaluationRepository
from b2speak_api.infrastructure.mongodb_repositories.user import MongoUserRepository
from b2speak_api.infrastructure.azure_blob_storage import AzureBlobStorage
from b2speak_api.application.use_cases.speak_evaluation import UploadSpeakEvaluationUseCase

load_dotenv()

def get_speaking_image_use_case(request : Request) -> SpeakingImageUseCase:

    database = request.app.state.mongo_client[os.getenv("MONGO_DB")]
    storage = request.app.state.azure_storage
    repository = MongoSpeakingImageRepository(database["SpeakingImage"])

    return SpeakingImageUseCase(repository, storage)

def get_speak_evaluation_use_case(request : Request) -> UploadSpeakEvaluationUseCase:

    database = request.app.state.mongo_client[os.getenv("MONGO_DB")]
    storage = request.app.state.azure_storage
    repository = MongoSpeakEvaluationRepository(database["SpeakEvaluation"])

    return UploadSpeakEvaluationUseCase(repository, storage, get_speaking_image_use_case(request).repository)


def get_user_use_case(request : Request) -> UserUseCase:

    database = request.app.state.mongo_client[os.getenv("MONGO_DB")]
    storage = request.app.state.azure_storage
    repository = MongoUserRepository(database["User"])

    return UserUseCase(repository, storage)

