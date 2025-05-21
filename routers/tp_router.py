from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from uuid import UUID
from db.db_connection import AsyncSession, get_db
from routers.models.request_models import ApartmentCreate, ApartmentFilter, ApartmentUpdate
from auth.auth_services import user_dependency
from logger import get_logger
from db.flats_repository import apartment_repository

logger = get_logger(__name__)

apartment_router = APIRouter(
    prefix='/apartments',
    tags=['Apartments']
)

@apartment_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_apartment(
    apartment_data: ApartmentCreate,
    current_user: user_dependency
):
    try:
        return await apartment_repository.create_apartment(apartment_data.dict())
    except Exception as e:
        logger.error(f"Error creating apartment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create apartment"
        )

@apartment_router.get("/{apartment_id}")
async def get_apartment(
    apartment_id: UUID
):
    apartment = await apartment_repository.get_apartment_by_id(apartment_id)
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return apartment

@apartment_router.put("/{apartment_id}")
async def update_apartment(
    apartment_id: UUID, 
    update_data: ApartmentUpdate,
):
    apartment = await apartment_repository.update_apartment(apartment_id, update_data.dict(exclude_unset=True))
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return apartment

@apartment_router.get("/")
async def list_apartments(
    current_user: user_dependency,
    skip: int = 0, 
    limit: int = 100,
    ):
    return await apartment_repository.get_all_apartments(skip=skip, limit=limit)

@apartment_router.get("/seller/{seller_id}")
async def get_seller_apartments(
    seller_id: UUID,):
    return await apartment_repository.get_apartments_by_seller(seller_id)

@apartment_router.get("/count/total")
async def count_apartmen():
    return await apartment_repository.count_all_flats()

@apartment_router.get("/count/region/{region}")
async def count_apartments_by_region(
    region: str, 
    rooms: Optional[int] = None,):
    return await apartment_repository.count_flats_by_region(region=region, rooms=rooms)

@apartment_router.post("/filter")
async def filter_apartments(
    filters: ApartmentFilter,):
    return await apartment_repository.get_flats_with_filters(
        city=filters.city,
        min_price=filters.min_price,
        max_price=filters.max_price,
        rooms=filters.rooms,
        skip=filters.skip,
        limit=filters.limit
    )

@apartment_router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_apartment(
    apartment_id: int,):
    apartment = await apartment_repository.deactivate_apartment(apartment_id)
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return None