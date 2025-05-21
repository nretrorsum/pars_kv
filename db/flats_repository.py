from sqlalchemy import select, func, desc, distinct, delete
from db.db_connection import async_session
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from db.model import Apartment
from db.db_connection import AsyncSession
from logger import get_logger

logger = get_logger(__name__)


class ApartmentRepository():
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def _get_last_date(self, session: AsyncSession) -> Optional[datetime]:
        """Допоміжний метод для отримання останньої дати додавання"""
        query = (
            select(distinct(Apartment.listed_date))
            .order_by(desc(Apartment.listed_date))
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalar()

    async def create_apartment(self, apartment_data: dict) -> Apartment:
        """Створити нову квартиру"""
        async with self.session_factory() as session:
            async with session.begin():
                new_apartment = Apartment(
                    title=apartment_data["title"],
                    description=apartment_data.get("description"),
                    price=apartment_data["price"],
                    currency=apartment_data.get("currency", "USD"),
                    address=apartment_data["address"],
                    city=apartment_data["city"],
                    region=apartment_data.get("region"),
                    postal_code=apartment_data.get("postal_code"),
                    rooms=apartment_data["rooms"],
                    floor=apartment_data.get("floor"),
                    total_floors=apartment_data.get("total_floors"),
                    area=apartment_data["area"],
                    living_area=apartment_data.get("living_area"),
                    kitchen_area=apartment_data.get("kitchen_area"),
                    year_built=apartment_data.get("year_built"),
                    building_type=apartment_data.get("building_type"),
                    condition=apartment_data.get("condition"),
                    has_balcony=apartment_data.get("has_balcony", False),
                    is_furnished=apartment_data.get("is_furnished", False),
                    seller_id=apartment_data["seller_id"],
                    listed_date=datetime.utcnow(),
                    is_active=True
                )
                session.add(new_apartment)
            await session.refresh(new_apartment)
            return new_apartment

    async def update_apartment(self, apartment_id: int, update_data: dict) -> Optional[Apartment]:
        """Оновити інформацію про квартиру"""
        async with self.session_factory() as session:
            async with session.begin():
                query = select(Apartment).where(Apartment.id == apartment_id)
                result = await session.execute(query)
                apartment = result.scalar_one_or_none()
                
                if not apartment:
                    return None
                
                for key, value in update_data.items():
                    if hasattr(apartment, key):
                        setattr(apartment, key, value)
                
                apartment.listed_date = datetime.utcnow()
            await session.refresh(apartment)
            return apartment

    async def get_apartment_by_id(self, apartment_id: int) -> Optional[Apartment]:
        """Отримати квартиру за ID"""
        async with self.session_factory() as session:
            query = select(Apartment).where(Apartment.id == apartment_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_all_apartments(self, skip: int = 0, limit: int = 100) -> List[Apartment]:
        """Отримати список всіх квартир"""
        async with self.session_factory() as session:
            query = select(Apartment).offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_apartments_by_seller(self, seller_id: UUID) -> List[Apartment]:
        """Отримати квартири конкретного продавця"""
        async with self.session_factory() as session:
            query = select(Apartment).where(Apartment.seller_id == seller_id)
            result = await session.execute(query)
            return result.scalars().all()

    async def count_all_flats(self) -> int:
        """Отримати загальну кількість квартир"""
        async with self.session_factory() as session:
            query = select(func.count(Apartment.id))
            result = await session.execute(query)
            return result.scalar()

    async def count_flats_by_region(self, region: str, rooms: Optional[int] = None) -> int:
        """Підрахувати квартири за регіоном та кількістю кімнат"""
        async with self.session_factory() as session:
            query = select(func.count(Apartment.id)).where(
                Apartment.region.ilike(f'%{region}%'),
                Apartment.is_active == True
            )
            
            if rooms is not None:
                query = query.where(Apartment.rooms == rooms)
                
            result = await session.execute(query)
            return result.scalar()

    async def deactivate_apartment(self, apartment_id: int) -> Optional[Apartment]:
        """Деактивувати квартиру (soft delete)"""
        async with self.session_factory() as session:
            async with session.begin():
                query = delete(Apartment).where(Apartment.id == apartment_id)
                result = await session.execute(query)
                logger.debug(f'Result of deleting(deactivating) apartment:{result}')
            return None

    async def get_flats_with_filters(
        self,
        city: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        rooms: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        """Отримати квартири з фільтрами"""
        async with self.session_factory() as session:
            query = select(Apartment).where(Apartment.is_active == True)
            
            if city:
                query = query.where(Apartment.city.ilike(f'%{city}%'))
            if min_price is not None:
                query = query.where(Apartment.price >= min_price)
            if max_price is not None:
                query = query.where(Apartment.price <= max_price)
            if rooms is not None:
                query = query.where(Apartment.rooms == rooms)
                
            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
        
apartment_repository = ApartmentRepository(async_session)