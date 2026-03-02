from azure.storage.blob.aio import BlobServiceClient

class AzureBlobStorage:

    def __init__(self, connection_string: str, container_name: str):
        self.client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name

    async def upload(self, file_name: str, content: bytes) -> str:
        container = self.client.get_container_client(self.container_name)
        blob = container.get_blob_client(file_name)

        await blob.upload_blob(content, overwrite=True)

        return blob.url

    async def close(self):
        await self.client.close()
