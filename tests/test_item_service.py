from decimal import Decimal

import pytest

from app.application.services.item_service import ItemService
from app.domain.entities.item import Item
from app.schemas.item import ItemCreate, ItemPaginationQuery, ItemUpdate


class FakeItemRepository:
    def __init__(self) -> None:
        self.items = [
            Item(
                id="1",
                name="Keyboard",
                description="Mechanical keyboard",
                price=Decimal("120.50"),
                quantity=4,
            ),
            Item(
                id="2",
                name="Mouse",
                description="Wireless mouse",
                price=Decimal("60.00"),
                quantity=10,
            ),
        ]

    async def create(self, item: Item) -> Item:
        created = Item(
            id="3",
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self.items.append(created)
        return created

    async def list_paginated(self, skip: int, limit: int) -> tuple[list[Item], int]:
        return self.items[skip : skip + limit], len(self.items)

    async def get_by_id(self, item_id: str) -> Item:
        return next(item for item in self.items if item.id == item_id)

    async def update(self, item_id: str, payload: dict) -> Item:
        item = await self.get_by_id(item_id)
        updated = Item(
            id=item.id,
            name=payload.get("name", item.name),
            description=payload.get("description", item.description),
            price=payload.get("price", item.price),
            quantity=payload.get("quantity", item.quantity),
        )
        self.items = [updated if existing.id == item_id else existing for existing in self.items]
        return updated

    async def delete(self, item_id: str) -> None:
        self.items = [item for item in self.items if item.id != item_id]


@pytest.mark.asyncio
async def test_list_items_returns_pagination_metadata() -> None:
    service = ItemService(FakeItemRepository())

    response = await service.list_items(ItemPaginationQuery(page=1, page_size=1))

    assert response.meta.total_items == 2
    assert response.meta.total_pages == 2
    assert response.meta.has_next is True
    assert len(response.data) == 1


@pytest.mark.asyncio
async def test_create_item_returns_created_record() -> None:
    service = ItemService(FakeItemRepository())

    created = await service.create_item(
        ItemCreate(
            name="Monitor",
            description="4K display",
            price=Decimal("320.00"),
            quantity=2,
        )
    )

    assert created.id == "3"
    assert created.name == "Monitor"


@pytest.mark.asyncio
async def test_update_item_applies_partial_changes() -> None:
    service = ItemService(FakeItemRepository())

    updated = await service.update_item("1", ItemUpdate(quantity=8))

    assert updated.id == "1"
    assert updated.quantity == 8
    assert updated.name == "Keyboard"

