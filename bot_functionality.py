import aiohttp
from logger import get_logger
from config import API_URL

logger = get_logger(__name__)


async def make_get_request(session: aiohttp.ClientSession, endpoint: str):
    try:
        async with session.get(f'{API_URL}{endpoint}') as response:
            logger.debug(f'GET request result:{str(response)}')
            return await response.json()
    except Exception as e:
        logger.error(f"Error in GET {endpoint}: {str(e)}")
        return {"error": str(e)}
    
async def make_post_request(session: aiohttp.ClientSession, endpoint: str, data: dict):
    try:
        async with session.post(f'{API_URL}{endpoint}', json=data) as response:
            logger.debug(f'POST request result:{str(response)}')
            return await response.json()
    except Exception as e:
        logger.error(f"Error in POST {endpoint}: {str(e)}")
        return {"error": str(e)}
    
async def get_general_stats(session):
    """Отримуємо загальну статистику"""
    return {
        'total_count': await make_get_request(session, '/flats/count'),
        'avg_prices': await make_post_request(session, '/flats/avg_price_by_rooms', {})
    }

async def get_stats_by_regions(session, regions):
    """Статистика по районах"""
    stats = {}
    for region in regions:
        data = {'region': region}
        stats[region] = {
            'count': await make_post_request(session, '/flats/count_by_region_rooms', data),
            'avg_price': await make_post_request(session, '/flats/avg_price_by_rooms_region', data),
            'price_per_sqm': await make_post_request(session, '/flats/avg_price_per_sqm', data)
        }
    return stats

async def get_stats_by_rooms(session, rooms):
    """Статистика по кімнатах"""
    stats = {}
    for rooms_count in rooms:
        data = {'rooms': rooms_count}
        stats[rooms_count] = {
            'count': await make_post_request(session, '/flats/count_by_region_rooms', data),
            'avg_price': await make_post_request(session, '/flats/avg_price_by_rooms', data)
        }
    return stats

async def get_stats_by_region_and_rooms(session, regions, rooms):
    """Статистика по районах і кімнатах"""
    stats = {}
    for region in regions:
        stats[region] = {}
        for rooms_count in rooms:
            data = {'region': region, 'rooms': rooms_count}
            stats[region][rooms_count] = {
                'count': await make_post_request(session, '/flats/count_by_region_rooms', data),
                'avg_price': await make_post_request(session, '/flats/avg_price_by_rooms_region', data)
            }
    return stats

def generate_full_report(data):
    """Генерує повний звіт у HTML форматі"""
    report = ["<b>📊 Повна аналітика нерухомості</b>\n"]
    
    # Загальна статистика
    report.append("\n<b>🏙 Загальна статистика по місту:</b>")
    report.append(f"• Всього оголошень: <b>{data['general']['total_count'].get('count', 'N/A')}</b>")
    
    # Статистика по кімнатах
    report.append("\n<b>🚪 Статистика за кількістю кімнат:</b>")
    for rooms_count, stats in data['by_rooms'].items():
        report.append(
            f"• {rooms_count}-кімнатні: "
            f"<b>{stats['count'].get('count', 'N/A')}</b> оголошень, "
            f"середня ціна <b>{stats['avg_price'].get('avg_price', 'N/A')} грн</b>"
        )
    
    # Статистика по районах
    report.append("\n<b>🏘 Статистика по районах:</b>")
    for region, stats in data['by_region'].items():
        report.append(
            f"\n<b>{region}:</b>\n"
            f"• Оголошень: <b>{stats['count'].get('count', 'N/A')}</b>\n"
            f"• Середня ціна: <b>{stats['avg_price'].get('avg_price', 'N/A')} грн</b>\n"
            f"• Ціна за м²: <b>{stats['price_per_sqm'].get('avg_price_per_sqm', 'N/A')} грн/м²</b>"
        )
    
    # Детальна статистика по районах і кімнатах
    report.append("\n<b>🔍 Детальна статистика (район × кімнати):</b>")
    for region, rooms_data in data['by_region_and_rooms'].items():
        report.append(f"\n<b>{region}:</b>")
        for rooms_count, stats in rooms_data.items():
            report.append(
                f"• {rooms_count}-кімнатні: "
                f"<b>{stats['count'].get('count', 'N/A')}</b> оголошень, "
                f"середня ціна <b>{stats['avg_price'].get('avg_price', 'N/A')} грн</b>"
            )
    
    return "\n".join(report)