from fastapi import APIRouter
from db.analyze_repository import rieltor_repository
from logger import get_logger

logger = get_logger(__name__)

flats_router = APIRouter(
    prefix = '/flats'
)

@flats_router.get('/districts')
async def return_flats_count(city: str = 'Lviv'):
    return str(await rieltor_repository.get_districts_by_city(city))

@flats_router.get('/marker_growth')
async def market_growth():
    # Отримуємо всі унікальні дати
    dates = await rieltor_repository.get_all_dates()
    
    # Отримуємо кількість квартир для кожної дати
    result = {}
    for date in dates:
        count = await rieltor_repository.count_flats_for_date(date)
        result[date] = count

    #logger.debug(f'Result in market growth:{result}')

    # Сортуємо дати у зворотному хронологічному порядку (від нових до старих)
    sorted_dates = sorted(result.keys(), reverse=True)

    logger.debug(f'Result in market growth:{sorted_dates}')
    
    # Обчислюємо різниці між послідовними датами
    result_list = {}
    for i in range(len(sorted_dates)-1):
        current_date = sorted_dates[i]
        next_date = sorted_dates[i+1]
        difference = round(((result[current_date] - result[next_date])/result[next_date])*100, 2)
        result_list[f"{current_date} → {next_date}"] = difference
    
    return result_list