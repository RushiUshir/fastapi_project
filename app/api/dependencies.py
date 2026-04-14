from collections.abc import AsyncIterator

from fastapi import Depends

from app.application.services.item_service import ItemService
from app.core.database import Database
from app.infrastructure.repositories.mongo_item_repository import MongoItemRepository


async def get_database() -> AsyncIterator[Database]:
    database = Database.get_instance()
    yield database


async def get_item_service(
    database: Database = Depends(get_database),
) -> AsyncIterator[ItemService]:
    repository = MongoItemRepository(database.item_collection)
    yield ItemService(repository)
