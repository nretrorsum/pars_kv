from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class RequestFlatsByRegionAndRooms(BaseModel):
    region: str
    rooms: int
    
class RequestRooms(BaseModel):
    rooms: int
    
class RequestRegion(BaseModel):
    region: str
    
class RequestAdress(BaseModel):
    adress: str

# Pydantic моделі для запитів
class ApartmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    currency: Optional[str] = "USD"
    address: str
    city: str
    region: Optional[str] = None
    postal_code: Optional[str] = None
    rooms: int
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    area: float
    living_area: Optional[float] = None
    kitchen_area: Optional[float] = None
    year_built: Optional[int] = None
    building_type: Optional[str] = None
    condition: Optional[str] = None
    has_balcony: Optional[bool] = False
    is_furnished: Optional[bool] = False
    seller_id: UUID

class ApartmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    rooms: Optional[int] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    area: Optional[float] = None
    living_area: Optional[float] = None
    kitchen_area: Optional[float] = None
    year_built: Optional[int] = None
    building_type: Optional[str] = None
    condition: Optional[str] = None
    has_balcony: Optional[bool] = None
    is_furnished: Optional[bool] = None
    is_active: Optional[bool] = None

class ApartmentFilter(BaseModel):
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rooms: Optional[int] = None
    skip: int = 0
    limit: int = 100