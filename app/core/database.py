from pymongo import ASCENDING
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
from pymongo import AsyncMongoClient

from app.core.config import get_settings


class Database:
    _instance: "Database | None" = None

    def __init__(self) -> None:
        settings = get_settings()
        self.client = AsyncMongoClient(settings.mongodb_uri)
        self.database: AsyncDatabase = self.client[settings.mongodb_database]
        self.item_collection: AsyncCollection = self.database[settings.mongodb_items_collection]

    @classmethod
    def get_instance(cls) -> "Database":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def connect(self) -> None:
        await self.item_collection.create_index([("name", ASCENDING)])

    async def close(self) -> None:
        await self.client.aclose()
        Database._instance = None

