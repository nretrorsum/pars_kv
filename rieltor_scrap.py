import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

async def rieltor_scrap(url):
    # Створюємо сесію з потрібним User-Agent
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        async with session.get(url) as response:
            html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        # Знаходимо всі елементи <script> з типом "application/ld+json"
        script_tag = soup.find('script', type='application/ld+json')

        if script_tag:
            print("Знайдено JSON:")  # Дебаг
            print(script_tag.string)  # Виводимо сам JSON

            try:
                # Перетворюємо JSON з тексту в об'єкт Python
                json_data = json.loads(script_tag.string)
                print("JSON перетворено в об'єкт Python:") 
                print(json_data)  # Виводимо перетворений JSON
                
                apartments = []
                for item in json_data.get('itemListElement', []):
                    apartment = item.get('item', {})

                    # Виведення елементів для перевірки
                    print("Апартаменти:", apartment)

                    price = apartment.get('offers', {}).get('price', 'Null')
                    address = apartment.get('address', {}).get('streetAddress', 'Null')
                    city = apartment.get('address', {}).get('addressLocality', 'Null')
                    district = apartment.get('offers', {}).get('areaServed', {}).get('name', 'Null')
                    rooms = apartment.get('numberOfRooms', 'Null')
                    total_size = apartment.get('description', 'Null')
                    link = apartment.get('url', 'Null')
                    images = apartment.get('image', [])
                    geo_coordinates = apartment.get('geo', {})
                    latitude = geo_coordinates.get('latitude', 'Null')
                    longitude = geo_coordinates.get('longitude', 'Null')
                    accommodation_category = apartment.get('accommodationCategory', 'Null')
                    availability = apartment.get('offers', {}).get('availability', 'Null')
                    availability_starts = apartment.get('offers', {}).get('availabilityStarts', 'Null')
                    price_valid_until = apartment.get('offers', {}).get('priceValidUntil', 'Null')

                    # Шукаємо площу
                    size_row = soup.find('div', class_='catalog-card-details-row', string=lambda text: text and 'м²' in text)
                    if size_row:
                        total_area = size_row.find('span', class_ = '').text.strip() if size_row else 'Unknown'
                        print("Знайдено площу:", total_area)  # Дебаг
                    else:
                        total_area = 'Unknown'
                        print("Площа не знайдена.")  # Дебаг

                    # Шукаємо поверх
                    floor_row = soup.find('div', class_='catalog-card-details-row', string=lambda text: text and 'поверх' in text)
                    if floor_row:
                        floor_info = floor_row.find('span', class_ = '').text.strip() if floor_row else 'Unknown'
                        print("Знайдено поверх:", floor_info)  # Дебаг
                    else:
                        floor_info = 'Unknown'
                        print("Поверх не знайдено.")  # Дебаг

                    apartments.append({
                        'price': price,
                        'address': address,
                        'city': city,
                        'district': district,
                        'rooms': rooms,
                        'total_size': total_size,
                        'link': link,
                        'images': images,
                        'latitude': latitude,
                        'longitude': longitude,
                        'accommodation_category': accommodation_category,
                        'availability': availability,
                        'availability_starts': availability_starts,
                        'price_valid_until': price_valid_until,
                        'total_area': total_area,
                        'floor_info': floor_info,
                    })

                return apartments
            except json.JSONDecodeError:
                print("Помилка при декодуванні JSON.")
                return []
        else:
            print("JSON дані не знайдено.")
            return []
