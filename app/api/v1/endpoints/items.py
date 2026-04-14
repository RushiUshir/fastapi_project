from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_item_service
from app.application.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemPaginationQuery, ItemRead, ItemUpdate
from app.shared.pagination import PaginatedResponse

router = APIRouter()


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service),
) -> ItemRead:
    return await service.create_item(payload)


@router.get("/", response_model=PaginatedResponse[ItemRead])
async def list_items(
    params: ItemPaginationQuery = Depends(),
    service: ItemService = Depends(get_item_service),
) -> PaginatedResponse[ItemRead]:
    return await service.list_items(params)


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: str,
    service: ItemService = Depends(get_item_service),
) -> ItemRead:
    return await service.get_item(item_id)


@router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: str,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
) -> ItemRead:
    return await service.update_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    service: ItemService = Depends(get_item_service),
) -> Response:
    await service.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

