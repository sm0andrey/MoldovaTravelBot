from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = [
    [KeyboardButton(text='Выбрать город')],
    [KeyboardButton(text='Помощь')]
]
kb_cities = [
        [KeyboardButton(text='Запросить город')],
        [KeyboardButton(text='Кишинёв')],
        [KeyboardButton(text='Тирасполь')],
        [KeyboardButton(text='Бельцы')]
    ]
kb_options = [
            [KeyboardButton(text='Достопримечательности')],
            [KeyboardButton(text='Погода')],
            [KeyboardButton(text='Назад')]
        ]