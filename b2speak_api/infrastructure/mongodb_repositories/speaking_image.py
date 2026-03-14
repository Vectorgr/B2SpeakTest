from b2speak_api.domain.repositories.speaking_image import SpeakingImageRepository
from b2speak_api.domain.models.speaking_image import SpeakingImage, SpeakingImageCreate
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

class MongoSpeakingImageRepository(SpeakingImageRepository):

    def __init__(self, collection : AsyncIOMotorCollection):
        self.collection = collection

    async def add(self, speaking_image: SpeakingImageCreate) -> SpeakingImage:
        inserted = await self.collection.insert_one(speaking_image.__dict__)
        print(f"Inserted document with ID: {inserted.inserted_id}")
        doc = await self.collection.find_one({'_id': inserted.inserted_id})
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return SpeakingImage(**doc)

    async def get(self, id: str) -> SpeakingImage | None:
        print(f"Fetching document with ID: {id}")
        obj_id = ObjectId(id)
        doc = await self.collection.find_one({'_id': obj_id})
        if doc:
            doc['_id'] = str(doc['_id'])
            return SpeakingImage(**doc)
        return None
    
    async def get_random(self) -> SpeakingImage | None:
            print("Fetching random document")
            docs = await self.collection.aggregate([{'$sample': {'size': 1}}]).to_list(length=1)
            if docs:
                print(f"Random document: {docs[0]}")
                doc = docs[0]
                doc['_id'] = str(doc['_id'])
                print(f"Returning document with ID: {doc['_id']}")
                return SpeakingImage(**doc)
            return None

