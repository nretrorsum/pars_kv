import requests
from bs4 import BeautifulSoup
import re
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from db.model import Flats
import uuid
from datetime import datetime

logging.basicConfig()

async def parse_flats(session: AsyncSession, page: int):
    if page == 0:
        url = f"https://flatfy.ua/uk/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2"
    else:
        url = f"https://flatfy.ua/uk/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2?page={page}"
    
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        apartment_blocks = soup.find_all("div", class_="feed-layout__item-holder")

        for block in apartment_blocks:
            price_block = block.find("div", class_="realty-preview-price--main")
            if price_block:
                price = re.sub(r'[^\d]', '', price_block.text.strip())
            else:
                price = None  # Якщо ціна не знайдена, ставимо None

            sqm_block = block.find("div", class_="realty-preview-price--sqm")
            if sqm_block:
                price_per_sqm = re.sub(r'\D', '', sqm_block.text.strip())
            else:
                price_per_sqm = None  # Якщо площа не знайдена, ставимо None

            region_blocks = block.find_all("a", class_="realty-preview-sub-title")
            if region_blocks:
                region = ', '.join([region.text.strip() for region in region_blocks])
            else:
                region = None  # Якщо район не знайдений, ставимо None

            rooms_block = block.find_all("span", class_="realty-preview-info")
            if len(rooms_block) >= 1:
                rooms = rooms_block[0].text.strip()
            else:
                rooms = None  # Якщо кількість кімнат не знайдена, ставимо None

            floor = None
            if len(rooms_block) >= 2:
                floor = rooms_block[2].text.strip()

            square = None
            if len(rooms_block) >= 2:
                squares_list = rooms_block[1].text.strip().split('/')
                try:
                    squares_list = [float(x.strip().replace('м²', '').replace(' ', '')) for x in squares_list]
                    square = sum(squares_list)
                except ValueError:
                    square = None  # Якщо не вдалось розпарсити, ставимо None
            
            room_squares = None
            if len(rooms_block) >= 2:
                room_squares = rooms_block[1].text.strip()
                
            year = None
            if len(rooms_block) >= 2:
                year = rooms_block[5].text.strip()
            # Створюємо об'єкт Flats для збереження в базі
            flat = Flats(
                id=uuid.uuid4(),
                price=int(price) if price else 0,  # Якщо ціна None, ставимо 0
                price_per_sqm=int(price_per_sqm) if price_per_sqm else 0,  # Якщо площа None, ставимо 0
                district=region if region else '',  # Якщо район None, ставимо порожній рядок
                rooms=rooms if rooms else '',  # Якщо кількість кімнат None, ставимо порожній рядок
                floor=floor if floor else '',  # Якщо поверх None, ставимо порожній рядок
                square=int(square) if square else 0,  # Якщо площа None, ставимо 0
                room_squares=room_squares if room_squares else '',  # Якщо розмір кімнат None, ставимо порожній рядок
                year = year if year else '',
                date_of_scrap = datetime.today().date()
            )
            
            # Додаємо об'єкт у сесію
            session.add(flat)

        # Зберігаємо зміни в базі даних
        await session.commit()
        print(year)
        logging.info(f"Page {page} data inserted.")
    else:
        logging.info(f"Не вдалося завантажити сторінку {page}!")
