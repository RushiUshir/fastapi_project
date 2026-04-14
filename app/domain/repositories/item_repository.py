from abc import ABC, abstractmethod

from app.domain.entities.item import Item


class ItemRepository(ABC):
    @abstractmethod
    async def create(self, item: Item) -> Item:
        raise NotImplementedError

    @abstractmethod
    async def list_paginated(self, skip: int, limit: int) -> tuple[list[Item], int]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, item_id: str) -> Item:
        raise NotImplementedError

    @abstractmethod
    async def update(self, item_id: str, payload: dict) -> Item:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item_id: str) -> None:
        raise NotImplementedError

