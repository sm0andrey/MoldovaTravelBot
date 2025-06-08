import aiohttp
import time
import datetime
import requests
from asyncio import Lock
from config.weather_settings import weather_config
lock=Lock()
class CityWeather:
    def __init__(self, cache_ttl: int = 600):

        self._weather_cache: dict[int,  dict] = {} # page -> (timestamp, data)
        self.cache_ttl = cache_ttl  # Время жизни кэша в секундах

    async def get_weather(self, city:str):
        now = time.time()

        if city in self._weather_cache:
            async with lock:
                ts, data = self._weather_cache[city]
                if now - ts < self.cache_ttl:
                    return data


        else:
            async with lock:
                response = requests.get(
                    f"http://api.openweathermap.org/data/2.5/weather?q={city.lower()}&lang=ru&units=metric&appid={weather_config.weather_api}")
                data = response.json()

                # 3. Сохраняем в кэш
                self._weather_cache[city] = (now, data)
                return data