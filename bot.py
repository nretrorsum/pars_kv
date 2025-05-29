import asyncio
from logger import get_logger
import sys
import aiohttp
from config import TG_SECRET as BOT_TOKEN
from config import API_URL
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_functionality import (get_general_stats, get_stats_by_region_and_rooms, 
                               get_stats_by_regions, get_stats_by_rooms, generate_full_report) 
import json

#BOT_TOKEN =  '7365543120:AAFdUOIzpTB0TUyjF_qtHCiCXGLaTaoaqEQ'#'7729651316:AAGhuO1Pv024FNWhv3fwOX1fnXU4_pn5TS8'
#API_URL = "http://127.0.0.1:8000"  

logger = get_logger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class FlatStates(StatesGroup):
    waiting_for_rooms = State()
    waiting_for_region = State()
    waiting_for_region_rooms = State()
    get_flats_by_sqm_price_region = State()
    analytics = State()

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Загальна кількість квартир", callback_data="count_flats")
    kb.button(text="🛏️ Кількість за кількістю кімнат", callback_data="count_by_rooms")
    kb.button(text="📍 Кількість квартир за регіоном", callback_data="get_flats_by_region_rooms")
    kb.button(text="💰 Середня ціна за кімнати", callback_data="avg_price_by_rooms")
    kb.button(text="📏 Ціна за м²", callback_data="avg_price_per_sqm")
    kb.button(text="Топ квартир по ціні за м2 і району", callback_data="get_flats_by_sqm_price_region")
    kb.button(text = 'Аналітика ринку', callback_data = 'analytics')
    kb.adjust(2)
    return kb.as_markup()

@dp.message(CommandStart())
async def start_message(message: Message):
    await message.answer(f'Привіт, {message.from_user.full_name}! Обери дію:', reply_markup=main_menu())


@dp.callback_query()
async def process_callback(call: CallbackQuery, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        if call.data == "count_flats":
            logger.debug(f'Base URL for request:{API_URL}')
            async with session.get(f"{API_URL}/count") as response:
                logger.debug(f'Request on URL:{API_URL}/count')
                data = await response.json()
                await call.message.answer(f"🔢 Загальна кількість квартир: {data}")

        elif call.data == "count_by_rooms":
            await call.message.answer("🔢 Введіть кількість кімнат:")
            await state.set_state(FlatStates.waiting_for_rooms)

        elif call.data == "get_flats_by_region_rooms":
            await call.message.answer("📍 Введіть регіон:")
            await state.set_state(FlatStates.waiting_for_region)

        elif call.data == "avg_price_by_rooms":
            await call.message.answer("💰 Введіть кількість кімнат для розрахунку середньої ціни:")
            await state.set_state(FlatStates.waiting_for_rooms)

        elif call.data == "avg_price_per_sqm":
            async with session.post(f"{API_URL}/avg_price_per_sqm") as response:
                data = await response.json()
                await call.message.answer(f"📏 Середня ціна за м²: {data}")
                
        elif call.data == "get_flats_by_sqm_price_region":
            await call.message.answer("📍 Введіть регіон:")
            await state.set_state(FlatStates.get_flats_by_sqm_price_region)

        elif call.data == 'analytics':
            await state.set_state(FlatStates.analytics)

@dp.message(FlatStates.waiting_for_rooms)
async def get_count_by_rooms(message: Message, state: FSMContext):
    try:
        rooms = str(message.text)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/count_by_rooms?rooms={int(rooms)}") as response:
                data = await response.json()
                logger.debug(f'Response from server:{data}')
                await message.answer(f"🛏️ Кількість квартир з {rooms} кімнатами: {data}")
        await state.clear() 
    except ValueError:
        await message.answer("❌ Введіть коректне число.")

@dp.message(FlatStates.get_flats_by_sqm_price_region)
async def get_flats_by_sqm_price_region(message: Message, state: FSMContext):
    try:
        region = str(message.text)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{API_URL}/get_flats_by_sqm_price_region",
                    json={"region": region}
                ) as response:
                    logger.debug(f'Response from server:{response}')
                    data = await response.json()
                    for flat in data: 
                        short_description = (flat['description'][:200] + '...') if len(flat['description']) > 200 else flat['description']
                        response_text = (
                            f"🏠 Квартира у районі {flat['region']}\n"
                            f"🔢 Кімнат: {flat['rooms']}\n"
                            f"📏 Площа: {flat['total_size']} м²\n"
                            f"💰 Ціна: {flat['price']} ({flat['price_per_m2']} за м²)\n"
                            f"📝 Опис: {short_description}\n"
                            f"📍 Адреса: {flat['adress']}\n"
                            f"🔗 Детальніше: {flat['link']}"
                        )
                        await message.answer(response_text)
                        if flat['photos']:
                            await message.answer_photo(flat['photos'][0])
                    else:
                        await message.answer(f"🔍 Квартир у районі {region} не знайдено")
                await state.clear()
            except Exception as e:
                await message.answer(f'Error: {e}')
    except ValueError:
        await message.answer('Введіть правильний район')


@dp.message(FlatStates.waiting_for_region)
async def get_flats_by_region_rooms(message: Message, state: FSMContext):
    try:
        region = str(message.text)
        user_data = await state.get_data()
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://localhost:8001/bot/count_flats_by_rooms_region?received_region={region}") as response:
                logger.debug(f'Response:{response}')
                result = await response.json()
                await message.answer(
                    f"Кількість квартир в районі {region}:\n"
                    f"1 кімната: {result['1_room']}\n"
                    f"2 кімнати: {result['2_room']}\n"
                    f"3 кімнати: {result['3_room']}\n"
                    f"4 кімнати: {result['4_room']}\n"
                    f"Всього: {result['total']}"
)
        await state.clear()  
    except ValueError:
        await message.answer("❌ Введіть коректне число.")

@dp.message(FlatStates.waiting_for_rooms)
async def get_avg_price_by_rooms(message: Message, state: FSMContext):
    try:
        rooms = int(message.text)
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/avg_price_by_rooms", json={"rooms": rooms}) as response:
                data = await response.json()
                await message.answer(f"💰 Середня ціна квартир з {rooms} кімнатами: {data}")
        await state.clear() 
    except ValueError:
        await message.answer("❌ Введіть коректне число.")

@dp.message(FlatStates.analytics)
async def get_full_analytics(message: types.Message, state: FSMContext):
    try:
        url = "http://localhost:8001/bot/full_analytics"  # встав сюди свій URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        text_lines = []
        # Загальна інформація
        total = data['general']['total_count']
        text_lines.append(f"🏠 <b>Всього квартир:</b> {total}\n")

        text_lines.append("<b>Середня ціна за кімнатами:</b>")
        for rooms, avg_price in data['general']['avg_price_by_rooms'].items():
            text_lines.append(f"  {rooms} кімнат(и): {float(avg_price):,.2f} грн")
        text_lines.append("")

        text_lines.append("<b>Кількість квартир по районах:</b>")
        for region, info in data['by_region'].items():
            text_lines.append(f"  {region}: {info['count']} квартир")
        text_lines.append("")

        text_lines.append("<b>Кількість та середня ціна по кімнатах:</b>")
        for rooms, info in data['by_rooms'].items():
            text_lines.append(f"  {rooms} кімнат(и): {info['count']} квартир, середня ціна {float(info['avg_price']):,.2f} грн")
        text_lines.append("")

        text_lines.append("<b>За районом і кількістю кімнат:</b>")
        for region, rooms_info in data['by_region_and_rooms'].items():
            text_lines.append(f"🏙 <b>{region}:</b>")
            for rooms, stats in rooms_info.items():
                text_lines.append(f"  {rooms} кімнат(и): {stats['count']} квартир, середня ціна {float(stats['avg_price']):,.2f} грн")
            text_lines.append("")

        report = "\n".join(text_lines)
        await message.answer(report, parse_mode='HTML')

    except Exception as e:
        await message.answer("❌ Сталася помилка при отриманні аналітики.")
        # тут можна ще залогувати помилку, якщо треба


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
