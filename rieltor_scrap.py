import aiohttp
from bs4 import BeautifulSoup
import re
from logger import get_logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import JSON  # Додано для зберігання списку фото
import uuid
from datetime import datetime
from db.model import FlatsFromRieltor
import json

logger = get_logger(__name__)

async def parse_flats_from_rieltor(session: AsyncSession, page: int):
    if page == 0:
        url = "https://rieltor.ua/lvov/flats-sale/#11.22/49.8292/24.0003"
    else:
        url = f"https://rieltor.ua/lvov/flats-sale/?page={page}#11.22/49.8292/24.0003"

    async with aiohttp.ClientSession() as http_session:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            async with http_session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Не вдалося завантажити сторінку {page}! Статус: {response.status}")
                    return

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                cards = soup.find_all('div', class_='catalog-card')

                for card in cards:
                    try:
                        # Заголовок ціни
                        price_title = card.find('strong', class_='catalog-card-price-title')
                        price = price_title.text.strip() if price_title else 'Null'
                        price = int(re.sub(r'[^\d]', '', price)) if price != 'Null' else 0

                        # Деталі ціни
                        price_details = card.find('div', class_='catalog-card-price-details')
                        price_per_m2 = price_details.text.strip() if price_details else 'Null'
                        price_per_m2 = int(re.sub(r'[^\d]', '', price_per_m2)) if price_per_m2 != 'Null' else 0

                        # Адреса
                        address = card.find('div', class_='catalog-card-address')
                        address = address.text.strip() if address else ''

                        # Район
                        region_block = card.find('div', class_='catalog-card-region')
                        if region_block:
                            region_parts = region_block.find_all('a')
                            region = ', '.join([part.text.strip() for part in region_parts])
                        else:
                            region = ''
                            if address:
                                address_parts = address.split(',')
                                if len(address_parts) > 1:
                                    region = address_parts[1].strip()

                        # Кількість кімнат
                        rooms = card.find('div', class_='catalog-card-details-row')
                        rooms = rooms.find('span').text.strip() if rooms else 'Null'
                        try:
                            rooms = int(re.sub(r'[^\d]', '', rooms)) if rooms and rooms != 'Null' else 0
                        except ValueError:
                            rooms = 0
                            logger.warning(f"Не вдалося перетворити кількість кімнат на число: {rooms}")

                        # Площа
                        size = card.find_all('div', class_='catalog-card-details-row')
                        total_size = '0'
                        if len(size) > 1:
                            size = size[1].find('span')
                            if size:
                                size_text = size.text.strip()
                                numbers = re.findall(r'\d+', size_text)
                                if numbers:
                                    total_size = str(sum(int(num) for num in numbers))
                                else:
                                    logger.warning(f"Не вдалося знайти числа у рядку: {size_text}")

                        # Поверх
                        floor = card.find_all('div', class_='catalog-card-details-row')
                        floor_text = ''
                        if len(floor) > 2:
                            floor = floor[2].find('span')
                            floor_text = floor.text.strip() if floor else ''

                        # Опис
                        description = card.find('div', class_='catalog-card-description')
                        description_text = ''
                        if description:
                            description_span = description.find('span')
                            description_text = description_span.text.strip() if description_span else ''

                        # Посилання на квартиру
                        link = card.find('a', href=True)
                        link = "https://rieltor.ua" + link['href'] if link else ''

                        # Отримуємо всі фото квартири
                        photos = []
                        photo_slider = card.find('div', class_='offer-photo-slider') or card.find('div', class_='offer-photo-slider')
                        
                        if photo_slider:
                            # Головне фото
                            main_img = photo_slider.find('img', class_='offer-photo-slider-blurred-bg')
                            if main_img and main_img.get('src'):
                                photos.append(main_img['src'].replace('/crop/4x4/', '/'))
                            
                            # Всі інші фото
                            slides_container = photo_slider.find('div', {'data-slides-container': True})
                            if slides_container:
                                # Звичайні фото (jpg)
                                slide_images = slides_container.find_all('img', class_='offer-photo-slider-slide-image')
                                for img in slide_images:
                                    src = img.get('src')
                                    if src and src not in photos:
                                        photos.append(src.replace('/crop/500x375/', '/'))
                                
                                # WebP фото
                                sources = slides_container.find_all('source')
                                for source in sources:
                                    srcset = source.get('srcset')
                                    if srcset:
                                        first_url = srcset.split()[0]
                                        clean_url = first_url.split('?')[0].replace('/crop/500x375/', '/')
                                        if clean_url not in photos:
                                            photos.append(clean_url)

                        # Видаляємо дублікати
                        photos = list(dict.fromkeys(photos))

                        # Створюємо новий запис
                        flat = FlatsFromRieltor(
                            id=uuid.uuid4(),
                            price=price,
                            price_per_m2=price_per_m2,
                            adress=address,
                            region=region,
                            rooms=rooms,
                            total_size=total_size,
                            floor=floor_text,
                            description=description_text,
                            link=link,
                            photos=photos,  # Список фото як JSON
                            date_of_scrap=datetime.now().date(),
                        )
                        session.add(flat)

                    except Exception as e:
                        logger.error(f"Помилка при обробці картки: {e}")
                        continue

                await session.commit()
                logger.info(f"Дані зі сторінки {page} успішно додано до бази даних.")

        except Exception as e:
            logger.error(f"Помилка при парсингу сторінки {page}: {e}")