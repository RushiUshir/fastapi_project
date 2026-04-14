from decimal import Decimal

from bson import ObjectId
from fastapi import HTTPException, status
from pymongo.asynchronous.collection import AsyncCollection

from app.domain.entities.item import Item
from app.domain.repositories.item_repository import ItemRepository


class MongoItemRepository(ItemRepository):
    def __init__(self, collection: AsyncCollection) -> None:
        self.collection = collection

    async def create(self, item: Item) -> Item:
        document = self._to_document(item)
        result = await self.collection.insert_one(document)
        created = await self.collection.find_one({"_id": result.inserted_id})
        return self._to_entity(created)

    async def list_paginated(self, skip: int, limit: int) -> tuple[list[Item], int]:
        cursor = self.collection.find().sort("_id", -1).skip(skip).limit(limit)
        items = [self._to_entity(document) async for document in cursor]
        total = await self.collection.count_documents({})
        return items, total

    async def get_by_id(self, item_id: str) -> Item:
        object_id = self._parse_object_id(item_id)
        document = await self.collection.find_one({"_id": object_id})
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return self._to_entity(document)

    async def update(self, item_id: str, payload: dict) -> Item:
        object_id = self._parse_object_id(item_id)
        document = self._normalize_update_payload(payload)
        result = await self.collection.update_one({"_id": object_id}, {"$set": document})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        updated = await self.collection.find_one({"_id": object_id})
        return self._to_entity(updated)

    async def delete(self, item_id: str) -> None:
        object_id = self._parse_object_id(item_id)
        result = await self.collection.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    @staticmethod
    def _parse_object_id(item_id: str) -> ObjectId:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item id")
        return ObjectId(item_id)

    @staticmethod
    def _to_document(item: Item) -> dict:
        return {
            "name": item.name,
            "description": item.description,
            "price": str(item.price),
            "quantity": item.quantity,
        }

    @staticmethod
    def _normalize_update_payload(payload: dict) -> dict:
        if "price" in payload:
            payload["price"] = str(payload["price"])
        return payload

    @staticmethod
    def _to_entity(document: dict | None) -> Item:
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

        return Item(
            id=str(document["_id"]),
            name=document["name"],
            description=document.get("description"),
            price=Decimal(document["price"]),
            quantity=document["quantity"],
        )

