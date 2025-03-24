from fastapi import FastAPI
from main import parse_flats
from db.db_connection import get_db
from routers.flats_router import flats_router
from rieltor_scrap import parse_flats_from_rieltor
from db.db_connection import async_session
from auth.registration import auth_router

app = FastAPI()

app.include_router(
    flats_router,
    tags=['Flats']
)

app.include_router(
    auth_router,
    tags = ['Auth']
)

@app.get('/rieltor_parse')
async def rieltor_parse():
    async with async_session() as session:  # Create an instance of AsyncSession
        for page in range(0, 158):  # Проходимо по сторінках від 0 до 157
            await parse_flats_from_rieltor(session=session, page=page)
    return {'status': 'succeed'}

@app.get('/main')
async def get_info():
    total_pages = 99  # Вказуємо кількість сторінок для парсингу, можна змінити
    for page in range(1, total_pages + 1):
        async for session in get_db():
            await parse_flats(session, page)
    return {'status':'succeed'}