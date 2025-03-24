from db.abstract_repository import AbstractFlatsRepository
from db.db_connection import async_session
from sqlalchemy import select, func, desc, distinct
from db.model import FlatsFromRieltor
import logging

logging.basicConfig()

async def get_last_date():
    async with async_session() as session:
        query = (
            select(distinct(FlatsFromRieltor.date_of_scrap))
            .order_by(desc(FlatsFromRieltor.date_of_scrap))
        )
        
        result = await session.execute(query)
        return result.scalar()

class RieltorFlatsRepository(AbstractFlatsRepository):
    def __init__(self, db):
        self.db = db
        
    async def get_all_flats(self):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(func.count(FlatsFromRieltor.id))
                .where(FlatsFromRieltor.date_of_scrap == last_date)
                )
            result = await session.execute(query)
            return result.scalar()
        
    async def count_flats_by_region(self, region, rooms):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(func.count(FlatsFromRieltor.id))
                .where(
                    FlatsFromRieltor.region.ilike(f'%{region}%'),
                    FlatsFromRieltor.rooms == rooms,
                    FlatsFromRieltor.date_of_scrap == last_date
                )
            )
            logging.info(f'Query = {query}')
            result = await session.execute(query)
            
            return result.scalar()
                    
    async def count_flats_by_rooms(self, rooms: str):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(func.count(FlatsFromRieltor.id))
                .where(FlatsFromRieltor.rooms == rooms,
                       FlatsFromRieltor.date_of_scrap == last_date)
                )
            result = await session.execute(query)
            return result.scalar()

    async def get_flats_by_rooms_region(self, region, rooms):
        async with self.db as session:
            query = (
                select(FlatsFromRieltor)
                .where((FlatsFromRieltor.region.ilike(f'%{region}%')) & (FlatsFromRieltor.rooms == rooms))
                .order_by(desc(FlatsFromRieltor.price))
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_avg_price_by_rooms(self, rooms):
        async with self.db as session:
            query = (
                select(func.avg(FlatsFromRieltor.price))
                .where(FlatsFromRieltor.rooms == rooms)
            )
            result = await session.execute(query)
            return result.scalar()

    async def get_avg_price_by_rooms_region(self,rooms, region):
        async with self.db as session:
            query = (
                select(func.avg(FlatsFromRieltor.price))
                .where(FlatsFromRieltor.rooms == rooms,
                       FlatsFromRieltor.region.ilike(f'%{region}%')
                       )
            )
            result = await session.execute(query)
            return result.scalar()
    
    async def get_avg_price_per_m2(self):
        last_date = await get_last_date()
        async with self.db as session:
            query = (
                    select(func.avg(FlatsFromRieltor.price_per_m2))
                    .where(FlatsFromRieltor.date_of_scrap == last_date)
                )
            result = await session.execute(query)
            return result.scalar()
    
    async def get_flats_by_sqm_price(self):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(FlatsFromRieltor)
                .where(FlatsFromRieltor.date_of_scrap == last_date)
                .order_by(desc(FlatsFromRieltor.price_per_m2))
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_flats_by_sqm_price_region(self, region):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(FlatsFromRieltor)
                .where(FlatsFromRieltor.region.ilike(f'%{region}%'),
                       FlatsFromRieltor.date_of_scrap == last_date)
                .order_by(FlatsFromRieltor.price_per_m2)
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_flats_by_sqm_price_region_rooms(self, region, rooms):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(FlatsFromRieltor)
                .where(FlatsFromRieltor.region.ilike(f'%{region}%'),
                       FlatsFromRieltor.rooms == rooms,
                       FlatsFromRieltor.date_of_scrap == last_date)
                .order_by(FlatsFromRieltor.price_per_m2)
            )
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_flats_by_adress(self, adress: str):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(FlatsFromRieltor)
                .where(FlatsFromRieltor.adress.ilike(f'%{adress}%'),
                       FlatsFromRieltor.date_of_scrap == last_date)
            )
            result = await session.execute(query)
            return result.scalars().all()

    #async def 

rieltor_repository = RieltorFlatsRepository(async_session())