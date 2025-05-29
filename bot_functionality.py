import aiohttp
from logger import get_logger
from config import API_URL
from typing import List, Dict

logger = get_logger(__name__)


ENDPOINTS = {
    "total_count": "/flats/count",
    "avg_price_by_rooms": "/flats/avg_price_by_rooms",
    "count_by_region_rooms": "/flats/count_by_region_rooms",
    "avg_price_by_rooms_region": "/flats/avg_price_by_rooms_region",
    "price_per_sqm": "/flats/avg_price_per_sqm"
}


async def make_get_request(session: aiohttp.ClientSession, endpoint: str) -> dict:
    try:
        async with session.get(f'{API_URL}{endpoint}') as response:
            logger.debug(f'GET {endpoint} -> {response.status}')
            return await response.json()
    except Exception as e:
        logger.error(f"GET {endpoint} error: {str(e)}")
        return {"error": str(e)}


async def make_post_request(session: aiohttp.ClientSession, endpoint: str, data: dict) -> dict:
    try:
        async with session.post(f'{API_URL}{endpoint}', json=data) as response:
            logger.debug(f'POST {endpoint} data={data} -> {response.status}')
            return await response.json()
    except Exception as e:
        logger.error(f"POST {endpoint} error: {str(e)}")
        return {"error": str(e)}


async def get_general_stats(session: aiohttp.ClientSession) -> dict:
    """Загальна статистика по всіх оголошеннях"""
    return {
        'total_count': await make_get_request(session, ENDPOINTS["total_count"]),
        'avg_prices': await make_post_request(session, ENDPOINTS["avg_price_by_rooms"], {})
    }


async def get_stats_by_regions(session: aiohttp.ClientSession, regions: List[str]) -> Dict[str, dict]:
    """Статистика по районах"""
    stats = {}
    for region in regions:
        data = {'region': region}
        stats[region] = {
            'count': await make_post_request(session, ENDPOINTS["count_by_region_rooms"], data),
            'avg_price': await make_post_request(session, ENDPOINTS["avg_price_by_rooms_region"], data),
            'price_per_sqm': await make_post_request(session, ENDPOINTS["price_per_sqm"], data)
        }
    return stats


async def get_stats_by_rooms(session: aiohttp.ClientSession, rooms: List[str]) -> Dict[str, dict]:
    """Статистика по кількості кімнат"""
    stats = {}
    for room_count in rooms:
        data = {'rooms': room_count}
        stats[room_count] = {
            'count': await make_post_request(session, ENDPOINTS["count_by_region_rooms"], data),
            'avg_price': await make_post_request(session, ENDPOINTS["avg_price_by_rooms"], data)
        }
    return stats


async def get_stats_by_region_and_rooms(session: aiohttp.ClientSession, regions: List[str], rooms: List[str]) -> Dict[str, dict]:
    """Статистика по районах та кількості кімнат"""
    stats = {}
    for region in regions:
        stats[region] = {}
        for room_count in rooms:
            data = {'region': region, 'rooms': room_count}
            stats[region][room_count] = {
                'count': await make_post_request(session, ENDPOINTS["count_by_region_rooms"], data),
                'avg_price': await make_post_request(session, ENDPOINTS["avg_price_by_rooms_region"], data)
            }
    return stats


def generate_full_report(data: dict) -> str:
    """Генерація HTML-звіту"""
    report = ["<b>📊 Повна аналітика нерухомості</b>"]

    # Загальна статистика
    general = data['general']
    report.append("\n<b>🏙 Загальна статистика по місту:</b>")
    report.append(f"• Всього оголошень: <b>{general['total_count'].get('count', 'N/A')}</b>")

    # Кімнати
    report.append("\n<b>🚪 Статистика за кількістю кімнат:</b>")
    for rooms_count, stats in data['by_rooms'].items():
        report.append(
            f"• {rooms_count}-кімнатні: "
            f"<b>{stats['count'].get('count', 'N/A')}</b> оголошень, "
            f"середня ціна <b>{stats['avg_price'].get('avg_price', 'N/A')} грн</b>"
        )

    # Райони
    report.append("\n<b>🏘 Статистика по районах:</b>")
    for region, stats in data['by_region'].items():
        report.append(
            f"\n<b>{region}:</b>\n"
            f"• Оголошень: <b>{stats['count'].get('count', 'N/A')}</b>\n"
            f"• Середня ціна: <b>{stats['avg_price'].get('avg_price', 'N/A')} грн</b>\n"
            f"• Ціна за м²: <b>{stats['price_per_sqm'].get('avg_price_per_sqm', 'N/A')} грн/м²</b>"
        )

    # Комбінація район × кімнати
    report.append("\n<b>🔍 Детальна статистика (район × кімнати):</b>")
    for region, room_data in data['by_region_and_rooms'].items():
        report.append(f"\n<b>{region}:</b>")
        for rooms_count, stats in room_data.items():
            report.append(
                f"• {rooms_count}-кімнатні: "
                f"<b>{stats['count'].get('count', 'N/A')}</b> оголошень, "
                f"середня ціна <b>{stats['avg_price'].get('avg_price', 'N/A')} грн</b>"
            )

    return "\n".join(report)