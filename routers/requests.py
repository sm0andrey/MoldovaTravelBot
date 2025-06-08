from aiogram import F, Router
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.user_states import UserStates
from services import google_sheets
from routers import greeting
from asyncio import Lock
import datetime
import logging

router = Router()

lock = Lock()
us_req=[]
@router.message(UserStates.Request1_state)
async def get_city(message:Message, state: FSMContext):
    global us_req
    us_req = []
    async with lock:
        us_req.append(message.from_user.id)
        us_req.append(datetime.datetime.now().isoformat())
        us_req.append(message.text)
    await state.set_state(UserStates.Request2_state)
    kb = [
        [KeyboardButton(text='Пропустить')]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    await message.answer('Напишите список достопримечательностей, которые следует добавить, или нажмите Пропустить', reply_markup=keyboard)

@router.message(UserStates.Request2_state)
async def get_sights(message:Message, state: FSMContext):
    global us_req
    if message.text == 'Пропустить':
        await google_sheets.add_data(google_sheets.client,google_sheets.table, 'requests', us_req)
        async with lock:
            us_req.clear()
    else:
        async with lock:
            us_req.append(message.text)
        await google_sheets.add_data(google_sheets.client,google_sheets.table, 'requests', us_req)
        async with lock:us_req.clear()
    await message.answer('Запрос принят')
    await state.clear()
    await greeting.menu(message, FSMContext)
    await state.set_state(UserStates.Starting_state)
