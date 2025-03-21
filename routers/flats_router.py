from fastapi import APIRouter
from db.repository import repository
from routers.models.request_models import RequestFlatsByDistrictAndRooms, RequestRooms, RequestDistrict
from rieltor_scrap import rieltor_scrap

flats_router = APIRouter(
    prefix = '/flats'
)

@flats_router.get('/count')
async def count_flats():
    return await repository.get_all_flats()

@flats_router.get('/count_by_rooms')
async def count_flats_by_rooms(rooms: str):
    return await repository.count_flats_by_rooms(rooms)

@flats_router.post('/count_by_district_rooms')
async def count_flats_by_district(request: RequestFlatsByDistrictAndRooms):
    return await repository.count_flats_by_district(
        district=request.district, 
        rooms = request.rooms
        )
    
@flats_router.post("/get_flats_by_district_rooms")
async def get_flats_by_district_rooms(request: RequestFlatsByDistrictAndRooms):
    return await repository.get_flats_by_rooms_district(
        district = request.district,
        rooms = request.rooms
    )
    
@flats_router.post('/avg_price_by_rooms')
async def get_avg_price_by_rooms(request: RequestRooms):
    return await repository.get_avg_price_by_rooms(
        rooms=request.rooms
    )

@flats_router.post('/avg_price_by_rooms_district')
async def get_avg_price_by_rooms_district(request: RequestFlatsByDistrictAndRooms):
    return await repository.get_avg_price_by_rooms_district(
        rooms = request.rooms,
        district = request.district
    )
    
@flats_router.post("/avg_price_per_sqm")
async def get_avg_price_per_sqm():
    return await repository.get_avg_price_per_sqm()

@flats_router.post("/get_flats_by_sqm_price")
async def get_flats_by_sqm_price():
    return await repository.get_flats_by_sqm_price()

@flats_router.post("/get_flats_by_sqm_price_district")
async def get_flats_by_sqm_price_district(request: RequestDistrict):
    return await repository.get_flats_by_sqm_price_district(
        district=request.district
    )

@flats_router.post("/get_flats_by_sqm_price_district_rooms")
async def get_flats_by_sqm_price_district_rooms(request: RequestFlatsByDistrictAndRooms):
    return await repository.get_flats_by_sqm_price_district_rooms(
        district=request.district,
        rooms=request.rooms
    )
    
@flats_router.get('/test_rieltor')
async def test_rieltor(url_request: str):
    return await rieltor_scrap(url = url_request)
    