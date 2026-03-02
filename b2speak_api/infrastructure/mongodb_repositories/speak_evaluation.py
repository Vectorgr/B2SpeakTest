from b2speak_api.domain.repositories.speak_evaluation import SpeakEvaluationRepository
from b2speak_api.domain.models.speak_evaluation import SpeakEvaluation, SpeakEvaluationCreate
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

class MongoSpeakEvaluationRepository(SpeakEvaluationRepository):

    def __init__(self, collection : AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, speak_evaluation: SpeakEvaluationCreate) -> SpeakEvaluation:
        inserted = await self.collection.insert_one(speak_evaluation.__dict__)
        print(f"Inserted document with ID: {inserted.inserted_id}")
        doc = await self.collection.find_one({'_id': inserted.inserted_id})
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return SpeakEvaluation(**doc)

    async def get(self, id: str) -> SpeakEvaluation | None:
        print(f"Fetching document with ID: {id}")
        obj_id = ObjectId(id)
        doc = await self.collection.find_one({'_id': obj_id})
        if doc:
            doc['_id'] = str(doc['_id'])
            return SpeakEvaluation(**doc)
        return None

    async def findByFileName(self, filename: str) -> SpeakEvaluation | None:
        print(f"Fetching document with filename: {filename}")
        doc = await self.collection.find_one({'audio_name': filename})
        if doc:
            doc['_id'] = str(doc['_id'])
            return SpeakEvaluation(**doc)
        return None
    
    async def findByUserId(self, user_id: str) -> list[SpeakEvaluation]:
        print(f"Fetching documents with user_id: {user_id}")
        cursor = self.collection.find({'user_id': user_id})
        results = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            results.append(SpeakEvaluation(**doc))
        return results
    
    async def update(self, id: str, update_data: dict) -> SpeakEvaluation | None:
        obj_id = ObjectId(id)

        await self.collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )

        doc = await self.collection.find_one({"_id": obj_id})

        if doc:
            doc["_id"] = str(doc["_id"])
            return SpeakEvaluation(**doc)

        return None

