import logging

from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Dict, Awaitable, Any

# Создаем класс мидлвари, унаследованный от
# aiogram'овского BaseMiddleware
class MessageLog(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info(event.text) # Выводим текст сообщения
        return await handler(event, data) # Возвращаем обновление хендлерам

