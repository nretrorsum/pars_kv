from fastapi import APIRouter
from db.rieltor_repository import rieltor_repository
from routers.models.request_models import (RequestFlatsByRegionAndRooms, 
RequestRooms, RequestRegion, RequestAdress)

flats_router = APIRouter(
    prefix = '/flats'
)

@flats_router.get('/count')
async def count_flats():
    return await rieltor_repository.get_all_flats()

@flats_router.get('/count_by_rooms')
async def count_flats_by_rooms(rooms: str):
    return await rieltor_repository.count_flats_by_rooms(rooms)

@flats_router.post('/count_by_region_rooms')
async def count_flats_by_region(request: RequestFlatsByRegionAndRooms):
    return await rieltor_repository.count_flats_by_region(
        region=request.region, 
        rooms = request.rooms
        )
    
@flats_router.post("/get_flats_by_region_rooms")
async def get_flats_by_region_rooms(request: RequestFlatsByRegionAndRooms):
    return await rieltor_repository.get_flats_by_rooms_region(
        region = request.region,
        rooms = request.rooms
    )
    
@flats_router.post('/avg_price_by_rooms')
async def get_avg_price_by_rooms(request: RequestRooms):
    return await rieltor_repository.get_avg_price_by_rooms(
        rooms=request.rooms
    )

@flats_router.post('/avg_price_by_rooms_region')
async def get_avg_price_by_rooms_region(request: RequestFlatsByRegionAndRooms):
    return await rieltor_repository.get_avg_price_by_rooms_region(
        rooms = request.rooms,
        region = request.region
    )
    
@flats_router.post("/avg_price_per_sqm")
async def get_avg_price_per_sqm():
    return await rieltor_repository.get_avg_price_per_m2()

@flats_router.post("/get_flats_by_sqm_price")
async def get_flats_by_sqm_price():
    return await rieltor_repository.get_flats_by_sqm_price()

@flats_router.post("/get_flats_by_sqm_price_region")
async def get_flats_by_sqm_price_region(request: RequestRegion):
    return await rieltor_repository.get_flats_by_sqm_price_region(
        region=request.region
    )

@flats_router.post("/get_flats_by_sqm_price_region_rooms")
async def get_flats_by_sqm_price_region_rooms(request: RequestFlatsByRegionAndRooms):
    return await rieltor_repository.get_flats_by_sqm_price_region_rooms(
        region=request.region,
        rooms=request.rooms
    )
    
@flats_router.post('/get_flats_by_adress')
async def get_flats_by_adress(request: RequestAdress):
    return await rieltor_repository.get_flats_by_adress(request.adress)