from abc import ABC

class AbstractFlatsRepository(ABC):
    async def get_all_flats():
        raise NotImplementedError
    
    async def count_flats_by_district():
        raise NotImplementedError
    
    async def count_flats_by_rooms():
        raise NotImplementedError
    
    async def get_flats_by_district_rooms():
        raise NotImplementedError
    
    async def get_expencive():
        raise NotImplementedError
    
    async def get_cheapest():
        raise NotImplementedError
    
    async def get_avg_price_by_rooms():
        raise NotImplementedError
    
    async def get_avg_price_by_rooms_district():
        raise NotImplementedError
    