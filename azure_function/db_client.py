from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, Dict, Any
import os
from motor.motor_asyncio import AsyncIOMotorClient

from domain.models import SpeakEvaluation

class DbClient:
    def __init__(self):
        client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
        database = client[os.environ.get("MONGO_DB")]
        self.collection = database["SpeakEvaluation"]

    async def findByFileName(self, filename: str) -> SpeakEvaluation | None:
        doc = await self.collection.find_one({'audio_name': filename})
        if doc:
            doc['_id'] = str(doc['_id'])
            return SpeakEvaluation(**doc)
        return None
    
    async def update(self, id: str, update_data: dict) -> None:
        obj_id = ObjectId(id)

        await self.collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
