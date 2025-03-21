from pydantic import BaseModel

class RequestFlatsByDistrictAndRooms(BaseModel):
    district: str
    rooms: str
    
class RequestRooms(BaseModel):
    rooms: str
    
class RequestDistrict(BaseModel):
    district: str