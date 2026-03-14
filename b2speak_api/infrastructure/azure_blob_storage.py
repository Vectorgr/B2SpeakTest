from azure.storage.blob.aio import BlobServiceClient

class AzureBlobStorage():

    def __init__(self, connection_string: str, container_name_audios: str, container_name_speaking_images: str):
        print("Initializing AzureBlobStorage with connection string:", connection_string, "and container names:", container_name_audios, container_name_speaking_images)
        self.client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name_audios = container_name_audios
        self.container_name_speaking_images = container_name_speaking_images

    async def upload(self, file_name: str, content: bytes, container_name: str) -> str:
        container = self.client.get_container_client(container_name)
        blob = container.get_blob_client(file_name)

        await blob.upload_blob(content, overwrite=True)

        return blob.url
    
    async def upload_audio(self, file_name: str, content: bytes) -> str:
        return await self.upload(file_name, content, self.container_name_audios)
    
    async def upload_speaking_image(self, file_name: str, content: bytes) -> str:
        return await self.upload(file_name, content, self.container_name_speaking_images)

    async def download(self, file_name: str, container_name: str) -> bytes:
        container = self.client.get_container_client(container_name)
        blob = container.get_blob_client(file_name)

        stream = await blob.download_blob()
        return await stream.readall()
    
    async def download_audio(self, file_name: str) -> bytes:
        return await self.download(file_name, self.container_name_audios)
    
    async def download_speaking_image(self, file_name: str) -> bytes:
        return await self.download(file_name, self.container_name_speaking_images)
    
    async def close(self):
        await self.client.close()
