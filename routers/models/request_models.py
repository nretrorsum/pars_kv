from pydantic import BaseModel

class RequestFlatsByRegionAndRooms(BaseModel):
    region: str
    rooms: int
    
class RequestRooms(BaseModel):
    rooms: int
    
class RequestRegion(BaseModel):
    region: str
    
class RequestAdress(BaseModel):
    adress: str