from fastapi import APIRouter
from db.analyze_repository import rieltor_repository
from logger import get_logger
from typing import Dict, Any

logger = get_logger(__name__)

bot_united_router = APIRouter(
    prefix='/bot'
)

@bot_united_router.post('/count_flats_by_rooms_region')
async def flats_count_by_region(received_region: str):
    '''Count flats by certain region, que is straightforward'''
    result_list = []
    for i in range(1,5):
        rooms = await rieltor_repository.count_flats_by_region(region = received_region, rooms = int(i))
        result_list.append(rooms)

    total = await rieltor_repository.count_all_flats_by_region(region = received_region)
    result_list.append(total)
    return {
        '1_room': str(result_list[0]),
        '2_room': str(result_list[1]),
        '3_room': str(result_list[2]),
        '4_room': str(result_list[3]),
        'total': str(result_list[4]),
    }


REGIONS = ['Франківський', 'Залізничний', 'Шевченківський', 'Личаківський', 'Сихівський']
ROOMS = ['1', '2', '3', '4']

@bot_united_router.get("/full_analytics")
async def full_analytics() -> Dict[str, Any]:
    """
    Повна аналітика по районам та кількості кімнат
    """
    try:
        results = {
            'general': {},
            'by_region': {},
            'by_rooms': {},
            'by_region_and_rooms': {}
        }
        
        # Загальна статистика
        total_count = await rieltor_repository.get_all_flats()
        # Для середньої ціни за кількістю кімнат — збираємо по кожній кількості кімнат
        avg_price_by_rooms = {}
        for rooms in ROOMS:
            avg_price = await rieltor_repository.get_avg_price_by_rooms(int(rooms))
            avg_price_by_rooms[rooms] = avg_price
        results['general']['total_count'] = total_count
        results['general']['avg_price_by_rooms'] = avg_price_by_rooms

        # Статистика по районах
        for region in REGIONS:
            count_by_region = await rieltor_repository.count_all_flats_by_region(region)
            # Тобі потрібно додати метод get_avg_price_by_region у репозиторій
            avg_price_region = await rieltor_repository.get_avg_price_by_region(region=region)  # rooms=0 щоб отримати середню по регіону?
            
            price_per_sqm_region = await rieltor_repository.get_avg_price_per_m2_by_region(region = region)
            #price_per_sqm_region = None
            #avg_price_region = None 
            results['by_region'][region] = {
                'count': count_by_region,
                'avg_price': avg_price_region,
                'price_per_sqm': price_per_sqm_region,
            }

        # Статистика по кімнатах
        for rooms in ROOMS:
            count_by_rooms = await rieltor_repository.count_flats_by_rooms(int(rooms))
            avg_price_rooms = await rieltor_repository.get_avg_price_by_rooms(int(rooms))
            results['by_rooms'][rooms] = {
                'count': count_by_rooms,
                'avg_price': avg_price_rooms,
            }

        # Статистика по районах та кімнатах
        for region in REGIONS:
            results['by_region_and_rooms'][region] = {}
            for rooms in ROOMS:
                count = await rieltor_repository.count_flats_by_region(region, int(rooms))
                avg_price = await rieltor_repository.get_avg_price_by_rooms_region(int(rooms), region)
                results['by_region_and_rooms'][region][rooms] = {
                    'count': count,
                    'avg_price': avg_price,
                }

        return results

    except Exception as e:
        logger.error(f"Error in full_analytics endpoint: {e}")
        return {"error": "Internal server error"}