from app.domain.entities.item import Item
from app.domain.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemPaginationQuery, ItemRead, ItemUpdate
from app.shared.pagination import PaginatedResponse, PaginationMeta


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    async def create_item(self, payload: ItemCreate) -> ItemRead:
        item = Item(
            id=None,
            name=payload.name,
            description=payload.description,
            price=payload.price,
            quantity=payload.quantity,
        )
        created = await self.repository.create(item)
        return ItemRead.model_validate(created.to_dict())

    async def list_items(
        self,
        params: ItemPaginationQuery,
    ) -> PaginatedResponse[ItemRead]:
        skip = (params.page - 1) * params.page_size
        items, total = await self.repository.list_paginated(skip=skip, limit=params.page_size)
        total_pages = (total + params.page_size - 1) // params.page_size if total else 0

        return PaginatedResponse[ItemRead](
            data=[ItemRead.model_validate(item.to_dict()) for item in items],
            meta=PaginationMeta(
                page=params.page,
                page_size=params.page_size,
                total_items=total,
                total_pages=total_pages,
                has_previous=params.page > 1,
                has_next=params.page < total_pages,
            ),
        )

    async def get_item(self, item_id: str) -> ItemRead:
        item = await self.repository.get_by_id(item_id)
        return ItemRead.model_validate(item.to_dict())

    async def update_item(self, item_id: str, payload: ItemUpdate) -> ItemRead:
        item = await self.repository.update(item_id, payload.model_dump(exclude_unset=True))
        return ItemRead.model_validate(item.to_dict())

    async def delete_item(self, item_id: str) -> None:
        await self.repository.delete(item_id)
