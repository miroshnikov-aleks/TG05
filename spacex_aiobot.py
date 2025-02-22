from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
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

# Функция для обработки команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот, предоставляющий информацию о SpaceX. Доступные команды:\n\n"
        "/next_launch - Следующий запуск\n"
        "/rockets - Информация о ракетах\n"
        "/help - Помощь"
    )

# Функция для получения информации о следующем запуске
@dp.message(Command(commands=['next_launch']))
async def next_launch_info(message: types.Message):
    url = 'https://api.spacexdata.com/v4/launches/next'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        launch_message = (
            f"Следующий запуск запланирован на {data['date_local']} ({data['date_unix']}).\n"
            f"Название миссии: {data['name']}.\n"
            f"Детали: {data['details']}"
        )
        await message.answer(launch_message)
    else:
        await message.answer('Ой, похоже, что-то пошло не так.')

# Функция для получения информации о ракетах
@dp.message(Command(commands=['rockets']))
async def rockets_info(message: types.Message):
    url = 'https://api.spacexdata.com/v4/rockets'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rockets_list = '\n'.join(rocket['name'] for rocket in data)
        await message.answer(f"Ракеты SpaceX:\n{rockets_list}")
    else:
        await message.answer('Ой, похоже, что-то пошло не так.')

# Функция для помощи
@dp.message(Command(commands=['help']))
async def help_command(message: types.Message):
    await message.answer(
        "/next_launch - Следующий запуск\n"
        "/rockets - Информация о ракетах\n"
        "/help - Помощь"
    )

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
