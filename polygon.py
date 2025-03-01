import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from config import API_TOKEN, POLYGON_API_KEY

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# URL для Polygon.io API
POLYGON_BASE_URL = "https://api.polygon.io"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для получения текущей цены акции
def get_stock_price(ticker: str):
    url = f"{POLYGON_BASE_URL}/v2/aggs/ticker/{ticker}/prev"
    params = {
        "apiKey": POLYGON_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            price = data["results"][0]["c"]  # Цена закрытия
            return f"Текущая цена акции {ticker}: ${price}"
        else:
            return "Данные не найдены."
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к Polygon.io: {e}")
        return "Произошла ошибка при получении данных."

# Функция для получения новостей по тикеру
def get_stock_news(ticker: str):
    url = f"{POLYGON_BASE_URL}/v2/reference/news"
    params = {
        "ticker": ticker,
        "apiKey": POLYGON_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            news = "\n".join([f"{item['title']} - {item['article_url']}" for item in data["results"][:5]])
            return f"Новости по тикеру {ticker}:\n{news}"
        else:
            return "Новости не найдены."
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к Polygon.io: {e}")
        return "Произошла ошибка при получении новостей."

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот для работы с данными фондового рынка. Вот что я могу:\n"
        "/price [тиккер] — получить текущую цену акции.\n"
        "/news [тиккер] — получить последние новости по тикеру."
    )

# Обработчик команды /price
@dp.message(Command(commands=['price']))
async def handle_price(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите тикер акции. Пример: /price AAPL")
        return

    ticker = args[1].upper()
    result = get_stock_price(ticker)
    await message.answer(result)

# Обработчик команды /news
@dp.message(Command(commands=['news']))
async def handle_news(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите тикер акции. Пример: /news AAPL")
        return

    ticker = args[1].upper()
    result = get_stock_news(ticker)
    await message.answer(result)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))