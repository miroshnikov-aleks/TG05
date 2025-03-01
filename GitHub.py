from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging
import requests
from config import API_TOKEN

# Включаем логирование
logging.basicConfig(level=logging.INFO)

GITHUB_API_VERSION = "2022-11-28"
BASE_URL = "https://api.github.com"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для обработки команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот для работы с GitHub API. Вы можете использовать следующие команды:\n\n"
        "/get_user [имя пользователя] — Получить информацию о пользователе GitHub.\n"
        "/get_repo [владелец] [репозиторий] — Получить информацию о репозитории GitHub.\n\n"
        "Примеры использования:\n"
        "/get_user octocat — Информация о пользователе octocat.\n"
        "/get_repo octocat Hello-World — Информация о репозитории Hello-World от пользователя octocat."
    )

# Функция для выполнения запроса к GitHub API
async def fetch_github_data(endpoint: str):
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

# Функция для форматирования информации о пользователе
async def format_user_info(data):
    info = (
        f"Информация о пользователе:\n\n"
        f"Общие сведения:\n"
        f"- Имя пользователя: {data['login']}\n"
        f"- ID: {data['id']}\n"
        f"- Аватар: {data['avatar_url']}\n"
        f"- URL профиля: {data['html_url']}\n\n"
        f"Статистика:\n"
        f"- Подписчики: {data['followers']}\n"
        f"- Подписки: {data['following']}\n"
        f"- Репозитории: {data['public_repos']}\n\n"
        f"Дополнительные ссылки:\n"
        f"- Gists: {data['gists_url']}\n"
        f"- Starred репозитории: {data['starred_url']}\n"
        f"- Организации: {data['organizations_url']}\n"
        f"- События: {data['events_url']}\n"
        f"- Полученные события: {data['received_events_url']}"
    )
    return info

# Функция для форматирования информации о репозитории
async def format_repo_info(data):
    info = (
        f"Информация о репозитории:\n\n"
        f"Общие сведения:\n"
        f"- Название: {data['name']}\n"
        f"- Полное название: {data['full_name']}\n"
        f"- Язык: {data['language']}\n"
        f"- Владелец: {data['owner']['login']}\n"
        f"- URL репозитория: {data['html_url']}\n\n"
        f"Статистика:\n"
        f"- Звезд: {data['stargazers_count']}\n"
        f"- Наблюдателей: {data['watchers_count']}\n"
        f"- Форков: {data['forks_count']}\n"
        f"- Открытых вопросов: {data['open_issues_count']}\n\n"
        f"Даты:\n"
        f"- Создан: {data['created_at']}\n"
        f"- Последнее обновление: {data['updated_at']}\n"
        f"- Последний пуш: {data['pushed_at']}\n\n"
        f"Дополнительные ссылки:\n"
        f"- Клонирование: {data['clone_url']}\n"
        f"- SSH URL: {data['ssh_url']}\n"
        f"- Ветки: {data['branches_url']}\n"
        f"- Релизы: {data['releases_url']}"
    )
    return info

# Функция для отправки больших сообщений частями
async def send_large_message(message: types.Message, text: str, chunk_size=4000):
    for i in range(0, len(text), chunk_size):
        await message.answer(text[i:i+chunk_size])

# Обработчик для получения информации о пользователе
@dp.message(Command(commands=['get_user']))
async def handle_get_user(message: types.Message):
    username = message.text.split()[1] if len(message.text.split()) > 1 else None
    if username:
        data = await fetch_github_data(f"users/{username}")
        if data:
            formatted_info = await format_user_info(data)
            await send_large_message(message, formatted_info)
        else:
            await message.answer("Пользователь не найден или произошла ошибка.")
    else:
        await message.answer("Пожалуйста, укажите имя пользователя.")

# Обработчик для получения информации о репозитории
@dp.message(Command(commands=['get_repo']))
async def handle_get_repo(message: types.Message):
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Пожалуйста, укажите владельца и имя репозитория.\nПример: /get_repo octocat Hello-World")
        return

    owner = parts[1]
    repo = parts[2]

    data = await fetch_github_data(f"repos/{owner}/{repo}")
    if data:
        formatted_info = await format_repo_info(data)
        await send_large_message(message, formatted_info)
    else:
        await message.answer("Репозиторий не найден или произошла ошибка.")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))