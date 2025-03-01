import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from config import API_TOKEN, OPENWEATHER_API_KEY, UNSPLASH_API_KEY

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для получения прогноза погоды
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return {
            "description": weather_description,
            "temperature": temperature
        }
    except Exception as e:
        logging.error(f"Ошибка при получении данных о погоде: {str(e)}")
        return None

# Функция для получения изображения с Unsplash
def get_image(weather_condition: str):
    url = f"https://api.unsplash.com/photos/random?query={weather_condition}&orientation=landscape&client_id={UNSPLASH_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        image_url = data['urls']['regular']
        caption = data.get('alt_description', 'Описание недоступно')
        return {"image_url": image_url, "caption": caption}
    except Exception as e:
        logging.error(f"Ошибка при получении изображения: {str(e)}")
        return None

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для прогноза погоды.\n"
                        "Отправь название города, чтобы получить прогноз и фоновое изображение.")

# Обработчик текстовых сообщений
@dp.message()
async def handle_city(message: types.Message):
    city = message.text.strip()
    if not city:
        await message.reply("Пожалуйста, укажите название города.")
        return

    # Получаем прогноз погоды
    weather_data = get_weather(city)
    if not weather_data:
        await message.reply("Не удалось получить прогноз погоды. Проверьте название города и попробуйте снова.")
        return

    # Определяем тематику изображения на основе погоды
    weather_description = weather_data["description"]
    temperature = weather_data["temperature"]
    weather_keywords = {
        "дождь": "rain",
        "снег": "snow",
        "ясно": "sunny",
        "облачно": "cloudy"
    }
    weather_condition = "weather"  # По умолчанию
    for keyword, condition in weather_keywords.items():
        if keyword in weather_description.lower():
            weather_condition = condition
            break

    # Получаем изображение
    image_data = get_image(weather_condition)
    if not image_data:
        await message.reply("Не удалось получить изображение. Попробуйте снова.")
        return

    # Отправляем прогноз и изображение
    weather_message = (
        f"Прогноз погоды для города {city}:\n"
        f"Температура: {temperature}°C\n"
        f"Описание: {weather_description.capitalize()}"
    )
    await message.reply_photo(image_data["image_url"], caption=weather_message)

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)