from db.abstract_repository import AbstractFlatsRepository
from db.db_connection import async_session
from sqlalchemy import select, func, desc, distinct
from db.model import FlatsFromRieltor
from typing import Optional, List


class RieltorFlatsRepository(AbstractFlatsRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def _get_last_date(self, session) -> Optional[str]:
        """Допоміжний метод для отримання останньої дати скрапінгу"""
        query = (
            select(distinct(FlatsFromRieltor.date_of_scrap))
            .order_by(desc(FlatsFromRieltor.date_of_scrap))
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalar()

    async def get_all_flats(self) -> int:
        """Отримати загальну кількість квартир"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return 0
                    
                query = select(func.count(FlatsFromRieltor.id)).where(
                    FlatsFromRieltor.date_of_scrap == last_date
                )
                result = await session.execute(query)
                return result.scalar()
        
    async def count_flats_by_region(self, region: str, rooms: int) -> int:
        """Підрахувати квартири за регіоном та кількістю кімнат"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return 0
                    
                query = select(func.count(FlatsFromRieltor.id)).where(
                    FlatsFromRieltor.region.ilike(f'%{region}%'),
                    FlatsFromRieltor.rooms == rooms,
                    FlatsFromRieltor.date_of_scrap == last_date
                )
                result = await session.execute(query)
                return result.scalar()
                    
    async def count_flats_by_rooms(self, rooms: int) -> int:
        """Підрахувати квартири за кількістю кімнат"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return 0
                    
                # Явно вказуємо тип параметра для rooms
                query = select(func.count(FlatsFromRieltor.id)).where(
                    FlatsFromRieltor.rooms == rooms,  # Тепер порівнюємо integer з integer
                    FlatsFromRieltor.date_of_scrap == last_date
                )
                result = await session.execute(query)
                return result.scalar()

    async def get_flats_by_rooms_region(self, region: str, rooms: int) -> List[FlatsFromRieltor]:
        """Отримати квартири за кількістю кімнат та регіоном"""
        async with self.session_factory() as session:
            async with session.begin():
                query = select(FlatsFromRieltor).where(
                    FlatsFromRieltor.region.ilike(f'%{region}%'),
                    FlatsFromRieltor.rooms == rooms
                ).order_by(desc(FlatsFromRieltor.price))
                
                result = await session.execute(query)
                return result.scalars().all()
    
    async def get_avg_price_by_rooms(self, rooms: int) -> Optional[float]:
        """Отримати середню ціну за кількістю кімнат"""
        async with self.session_factory() as session:
            async with session.begin():
                query = select(func.avg(FlatsFromRieltor.price)).where(
                    FlatsFromRieltor.rooms == rooms
                )
                result = await session.execute(query)
                return result.scalar()

    async def get_avg_price_by_rooms_region(self, rooms: int, region: str) -> Optional[float]:
        """Отримати середню ціну за кількістю кімнат та регіоном"""
        async with self.session_factory() as session:
            async with session.begin():
                query = select(func.avg(FlatsFromRieltor.price)).where(
                    FlatsFromRieltor.rooms == rooms,
                    FlatsFromRieltor.region.ilike(f'%{region}%')
                )
                result = await session.execute(query)
                return result.scalar()
    
    async def get_avg_price_per_m2(self) -> Optional[float]:
        """Отримати середню ціну за квадратний метр"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return None
                    
                query = select(func.avg(FlatsFromRieltor.price_per_m2)).where(
                    FlatsFromRieltor.date_of_scrap == last_date
                )
                result = await session.execute(query)
                return result.scalar()
    
    async def get_flats_by_sqm_price(self) -> List[FlatsFromRieltor]:
        """Отримати квартири, відсортовані за ціною за квадратний метр"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return []
                    
                query = select(FlatsFromRieltor).where(
                    FlatsFromRieltor.date_of_scrap == last_date
                ).order_by(desc(FlatsFromRieltor.price_per_m2))
                
                result = await session.execute(query)
                return result.scalars().all()
    
    async def get_flats_by_sqm_price_region(self, region: str) -> List[FlatsFromRieltor]:
        """Отримати квартири за регіоном, відсортовані за ціною за квадратний метр"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return []
                    
                query = select(FlatsFromRieltor).where(
                    FlatsFromRieltor.region.ilike(f'%{region}%'),
                    FlatsFromRieltor.date_of_scrap == last_date
                ).order_by(FlatsFromRieltor.price_per_m2)
                page_size = 10  
                page_number = 1 
        
                query = query.limit(page_size).offset((page_number - 1) * page_size)
        
                result = await session.execute(query)
                return result.scalars().all()
    
    async def get_flats_by_sqm_price_region_rooms(self, region: str, rooms: int) -> List[FlatsFromRieltor]:
        """Отримати квартири за регіоном та кількістю кімнат, відсортовані за ціною за квадратний метр"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return []
                    
                query = select(FlatsFromRieltor).where(
                    FlatsFromRieltor.region.ilike(f'%{region}%'),
                    FlatsFromRieltor.rooms == rooms,
                    FlatsFromRieltor.date_of_scrap == last_date
                ).order_by(FlatsFromRieltor.price_per_m2)
                
                result = await session.execute(query)
                return result.scalars().all()
    
    async def get_flats_by_adress(self, adress: str) -> List[FlatsFromRieltor]:
        """Отримати квартири за адресою"""
        async with self.session_factory() as session:
            async with session.begin():
                last_date = await self._get_last_date(session)
                if not last_date:
                    return []
                    
                query = select(FlatsFromRieltor).where(
                    FlatsFromRieltor.adress.ilike(f'%{adress}%'),
                    FlatsFromRieltor.date_of_scrap == last_date
                )
                
                result = await session.execute(query)
                return result.scalars().all()

# Ініціалізація репозиторію
rieltor_repository = RieltorFlatsRepository(async_session)