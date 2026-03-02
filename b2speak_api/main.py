from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from b2speak_api.infrastructure.azure_blob_storage import AzureBlobStorage
from b2speak_api.interfaces.api import router
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os


app = FastAPI()
app.include_router(router)

# Store the storage instance globally for shutdown cleanup
storage_instance = None
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    app.state.mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    app.state.azure_storage = AzureBlobStorage(
        connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        container_name=os.getenv("AZURE_CONTAINER")
    )

@app.on_event("shutdown")
async def on_shutdown():
    if storage_instance:
        await storage_instance.close()

# How to run:
# poetry run uvicorn b2speak_api.main:app --reload