from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from states.user_states import UserStates
from aiogram.fsm.storage.memory import MemoryStorage
from routers import greeting
from services.weather import CityWeather
from services import google_sheets
from asyncio import Lock
from keyboards import builder
import datetime
import logging

lock = Lock()
router = Router()
weather=CityWeather()
cities=['Кишинёв', 'Тирасполь', 'Бельцы']
@router.message(UserStates.Starting_state, F.text == 'Выбрать город')
async def cmd_choose_city(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=builder.kb_cities)
    await state.set_state(UserStates.City_state)
    await message.answer('Какой город Вам интересен?', reply_markup = keyboard)

@router.message(UserStates.City_state)
async def cmd_choose_info(message:Message, state: FSMContext):
    if message.text in cities:
        keyboard = ReplyKeyboardMarkup(keyboard=builder.kb_options)
        await state.set_state(UserStates.Option_state)
        await state.update_data(chosen_city=message.text)
        await message.answer('Что Вы хотите узнать?', reply_markup=keyboard)
    elif message.text == 'Запросить город':
        await message.answer('Введите название города')
        await state.set_state(UserStates.Request1_state)


@router.message(UserStates.Option_state, F.text == 'Достопримечательности')
async def get_sights(message: Message, state: FSMContext):
    async with lock:
        user_data = await state.get_data()
        data=google_sheets.extract_data(google_sheets.table,user_data['chosen_city'],0)
    await message.answer_photo(photo=data['Photo'], caption=f"{data['Title']}\n{data['Description']}")
@router.message(UserStates.Option_state, F.text == 'Назад')
async def get_back(message: Message, state:FSMContext):
    await state.clear()
    await greeting.menu(message, FSMContext)
    await state.set_state(UserStates.Starting_state)
@router.message(UserStates.Option_state, F.text == 'Погода')
async def get_weather(message: Message, state:FSMContext):
    user_data = await state.get_data()
    async with lock:
        data = await weather.get_weather(city=user_data['chosen_city'])
        city = data["name"]
        cur_temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }
        weather_description = data["weather"][0]["main"]
        wd = code_to_smile[weather_description]
    await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
    )

