from db.abstract_repository import AbstractFlatsRepository
from db.db_connection import async_session
from sqlalchemy import select, func, desc, distinct
from db.model import Flats

async def get_last_date():
    async with async_session() as session:
        query = (
            select(distinct(Flats.date_of_scrap))
            .order_by(desc(Flats.date_of_scrap))
        )
        
        result = await session.execute(query)
        return result.scalar()

class FlatsRepository(AbstractFlatsRepository):
    def __init__(self, db):
        self.db = db
        
    async def get_all_flats(self):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(func.count(Flats.id))
                .where(Flats.date_of_scrap == last_date)
                )
            result = await session.execute(query)
            return result.scalar()
        
    async def count_flats_by_district(self, district, rooms):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(func.count(Flats.id))
                .where(
                    Flats.district.ilike(f'%{district}%'),
                    Flats.rooms == rooms,
                    Flats.date_of_scrap == last_date
                )
            )
            result = await session.execute(query)
            return result.scalar()
                    
    async def count_flats_by_rooms(self, rooms: str):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(func.count(Flats.id))
                .where(Flats.rooms == rooms,
                       Flats.date_of_scrap == last_date)
                )
            result = await session.execute(query)
            return result.scalar()

    async def get_flats_by_rooms_district(self, district, rooms):
        async with self.db as session:
            query = (
                select(Flats)
                .where((Flats.district.ilike(f'%{district}%')) & (Flats.rooms == rooms))
                .order_by(desc(Flats.price))
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_avg_price_by_rooms(self, rooms):
        async with self.db as session:
            query = (
                select(func.avg(Flats.price))
                .where(Flats.rooms == rooms)
            )
            result = await session.execute(query)
            return result.scalar()

    async def get_avg_price_by_rooms_district(self,rooms, district):
        async with self.db as session:
            query = (
                select(func.avg(Flats.price))
                .where(Flats.rooms == rooms,
                       Flats.district.ilike(f'%{district}%')
                       )
            )
            result = await session.execute(query)
            return result.scalar()
    
    async def get_avg_price_per_sqm(self):
        last_date = await get_last_date()
        async with self.db as session:
            query = (
                    select(func.avg(Flats.price_per_sqm))
                    .where(Flats.date_of_scrap == last_date)
                )
            result = await session.execute(query)
            return result.scalar()
    
    async def get_flats_by_sqm_price(self):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(Flats)
                .where(Flats.date_of_scrap == last_date)
                .order_by(desc(Flats.price_per_sqm))
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_flats_by_sqm_price_district(self, district):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(Flats)
                .where(Flats.district.ilike(f'%{district}%'),
                       Flats.date_of_scrap == last_date)
                .order_by(Flats.price_per_sqm)
            )
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_flats_by_sqm_price_district_rooms(self, district, rooms):
        async with self.db as session:
            last_date = await get_last_date()
            query = (
                select(Flats)
                .where(Flats.district.ilike(f'%{district}%'),
                       Flats.rooms == rooms,
                       Flats.date_of_scrap == last_date)
                .order_by(Flats.price_per_sqm)
            )
        result = await session.execute(query)
        return result.scalars().all()
    
    
repository = FlatsRepository(async_session())