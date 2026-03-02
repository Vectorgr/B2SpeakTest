from b2speak_api.domain.repositories.user import UserRepository
from b2speak_api.domain.models.user import User, UserCreate
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

class MongoUserRepository(UserRepository):

    def __init__(self, collection : AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, user: UserCreate) -> User:
        inserted = await self.collection.insert_one(user.__dict__)
        print(f"Inserted document with ID: {inserted.inserted_id}")
        doc = await self.collection.find_one({'_id': inserted.inserted_id})
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return User(**doc)

    async def get(self, id: str) -> User | None:
        print(f"Fetching document with ID: {id}")
        obj_id = ObjectId(id)
        doc = await self.collection.find_one({'_id': obj_id})
        if doc:
            doc['_id'] = str(doc['_id'])
            return User(**doc)
        return None

    async def get_by_email(self, email: str) -> User | None:
        print(f"Fetching document with email: {email}")
        doc = await self.collection.find_one({'email': email})
        if doc:
            doc['_id'] = str(doc['_id'])
            return User(**doc)
        return None

    async def update(self, id: str, update_data: dict) -> User | None:
        obj_id = ObjectId(id)

        await self.collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )

        doc = await self.collection.find_one({"_id": obj_id})

        if doc:
            doc["_id"] = str(doc["_id"])
            return User(**doc)

        return None

