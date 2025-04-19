from fastapi import FastAPI, Request
from main import parse_flats
from db.db_connection import get_db
from routers.flats_router import flats_router
from rieltor_scrap import parse_flats_from_rieltor
from db.db_connection import async_session
from auth.registration import auth_router
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("uvicorn")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
headers = ['Content-Type', 'Set-Cookie', 'Access-Control-Request-Headers',
                   'Access-Control-Allow-Origin', 'Authorization']

methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods= ['*'],
    allow_headers= ['*']
)

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    method = request.method
    url = request.url.path
    client_ip = request.client.host

    # Використовуємо стандартний метод логування без f-строк
    logger.info("New request: %s %s from %s", method, url, client_ip)

    response = await call_next(request)
    return response