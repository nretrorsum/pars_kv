from fastapi import FastAPI
from main import parse_flats
from db.db_connection import get_db
from routers.flats_router import flats_router

app = FastAPI()

app.include_router(
    flats_router,
    tags=['Flats']
)

@app.get('/main')
async def get_info():
    total_pages = 99  # Вказуємо кількість сторінок для парсингу, можна змінити
    for page in range(1, total_pages + 1):
        async for session in get_db():
            await parse_flats(session, page)
    return {'status':'succeed'}