from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters import Filter
from aiogram.types import Message
import asyncio
import logging
import requests

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Ваш токен бота
API_TOKEN = '8001285306:AAG9aTxJNrmgtFntvJUjgko5oaqwMwNbBnc'  # Замените на ваш токен от @BotFather

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем фильтр для текстовых сообщений
class TextStartsWithFilter(Filter):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def __call__(self, message: Message) -> bool:
        return message.text.startswith(self.prefix)

# Функция для обработки команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот, помогающий искать адреса в России. Начните вводить название региона, города или улицы, "
        "и я предложу варианты. Выберите нужный вариант, и я предоставлю подробную информацию."
    )

# Функция для поиска регионов
@dp.message(TextStartsWithFilter(prefix="регион "))
async def search_region(message: types.Message):
    query = message.text.split(maxsplit=1)[1]
    url = f'https://kladr-api.ru/api.php?query={query}&contentType=region'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        regions = '\n'.join(f"{item['name']}, {item['code']}" for item in data['result'])
        await message.answer(f"Найденные регионы:\n{regions}")
    else:
        await message.answer('Ой, похоже, что-то пошло не так.')

# Функция для поиска городов
@dp.message(TextStartsWithFilter(prefix="город "))
async def search_city(message: types.Message):
    query = message.text.split(maxsplit=1)[1]
    url = f'https://kladr-api.ru/api.php?query={query}&contentType=city'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cities = '\n'.join(f"{item['name']}, {item['code']}" for item in data['result'])
        await message.answer(f"Найденные города:\n{cities}")
    else:
        await message.answer('Ой, похоже, что-то пошло не так.')

# Функция для поиска улиц
@dp.message(TextStartsWithFilter(prefix="улица "))
async def search_street(message: types.Message):
    query = message.text.split(maxsplit=1)[1]
    url = f'https://kladr-api.ru/api.php?query={query}&contentType=street'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        streets = '\n'.join(f"{item['name']}, {item['code']}" for item in data['result'])
        await message.answer(f"Найденные улицы:\n{streets}")
    else:
        await message.answer('Ой, похоже, что-то пошло не так.')

# Функция для поиска домов
@dp.message(TextStartsWithFilter(prefix="дом "))
async def search_house(message: types.Message):
    query = message.text.split(maxsplit=1)[1]
    url = f'https://kladr-api.ru/api.php?query={query}&contentType=house'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        houses = '\n'.join(f"{item['name']}, {item['code']}" for item in data['result'])
        await message.answer(f"Найденные дома:\n{houses}")
    else:
        await message.answer('Ой, похоже, что-то пошло не так.')

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
