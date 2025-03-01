from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import requests
import logging
from config import API_TOKEN

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# URL вашего API на restninja.io
RESTNINJA_API_URL = 'http://httpbin.org/get'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для выполнения запроса к API restninja.io
def fetch_data_from_restninja():
    try:
        response = requests.get(RESTNINJA_API_URL)
        response.raise_for_status()  # Проверяем наличие ошибок HTTP
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return None

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот, который работает с API restninja.io. "
        "Отправьте команду /fetch, чтобы получить данные."
    )

# Обработчик команды /fetch
@dp.message(Command(commands=['fetch']))
async def fetch_data(message: types.Message):
    await message.answer("Запрашиваю данные из API...")
    data = fetch_data_from_restninja()
    if data:
        # Форматируем данные для отправки пользователю
        formatted_data = "\n".join([f"{key}: {value}" for key, value in data.items()])
        await message.answer(f"Данные из API:\n{formatted_data}")
    else:
        await message.answer("Извините, не удалось получить данные из API.")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))