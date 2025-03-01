import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from config import API_TOKEN, DADATA_API_KEY


# Включаем логирование
logging.basicConfig(level=logging.INFO)

# URL для DaData API
DADATA_API_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для выполнения поиска через DaData API
def fetch_dadata_data(query: str):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {
        "query": query,
        "count": 5  # Количество результатов
    }

    try:
        response = requests.post(DADATA_API_URL, json=data, headers=headers)
        response.raise_for_status()
        logging.info(f"Response from DaData API: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request failed: {e}")
        return None
    except ValueError as e:
        logging.error(f"JSON decoding failed: {e}")
        return None

# Функция для обработки команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот для поиска адресов. Введите запрос в формате: 'регион [название]', 'город [название]', 'улица [название] [город]', и я постараюсь найти для вас информацию."
    )

# Обработчик для поиска адресов
@dp.message()
async def handle_search(message: types.Message):
    if message.text is None:
        await message.answer("Извините, я не смог распознать ваш запрос. Пожалуйста, введите текст.")
        return

    text = message.text.lower()
    query = text

    data = fetch_dadata_data(query)
    if data and 'suggestions' in data:
        results = "\n".join([f"{item['value']}" for item in data['suggestions']])
        await message.answer(f"Результаты поиска:\n{results}")
    else:
        await message.answer('Извините, ничего не найдено. Попробуйте другой запрос.')

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))