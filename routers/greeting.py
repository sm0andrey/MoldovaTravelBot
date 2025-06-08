from aiogram import F, Router
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.user_states import UserStates
from keyboards import builder
import logging

router = Router()


@router.message(Command("start"), StateFilter(None))
async def greet(message: Message, state: FSMContext):
    await message.answer('Salut!!!\U0001F499\U0001F49B\U00002764')
    await state.set_state(UserStates.Starting_state)
    keyboard = ReplyKeyboardMarkup(keyboard=builder.kb_start)
    await message.answer('Что Вам нужно?', reply_markup = keyboard)

@router.message(Command("start"), StateFilter(None))
async def menu(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=builder.kb_start)
    await message.answer('Что Вам нужно?', reply_markup = keyboard)

@router.message(UserStates.Starting_state, F.text=='Помощь')
async def menu(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=builder.kb_start)
    await message.answer(f"Это бот MoldovaTravel!\nНажми Выбрать город и выбери интересующий тебя город из выпадающего списка. У каждого города ты можешь выбрать раздел Достопримечательности или Погода.\nЕсли интересующего тебя города в спике нет, нажми Запросить город. Бот спросит у тебя название города и его достопримечательности (этот пункт можно будет пропустить)")
    await message.answer('Что Вам нужно?', reply_markup = keyboard)