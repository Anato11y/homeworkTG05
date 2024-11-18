import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from googletrans import Translator

# Укажите свой токен Telegram-бота и API-ключ OMDb
TELEGRAM_TOKEN = "7555689186:AAElSVSvl9Nl931Iyw-1aR2Dz7TdU18pV_8"
OMDB_API_KEY = "c3205081"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()


# Функция для поиска информации о фильме
def get_movie_info(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
    return None


# Функция для перевода текста на русский язык
def translate_to_russian(text):
    translation = translator.translate(text, src="en", dest="ru")
    return translation.text


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Напиши название фильма, и я пришлю его описание, рейтинг и постер, а также переведу описание на русский язык.")


@dp.message()
async def send_movie_info(message: Message):
    movie_title = message.text
    movie_info = get_movie_info(movie_title)

    if movie_info:
        poster = movie_info.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
        description = movie_info['Plot']
        translated_description = translate_to_russian(description)

        info = (
            f"🎥 Название: {movie_info['Title']}\n"
            f"📅 Год: {movie_info['Year']}\n"
            f"🎭 Жанр: {movie_info['Genre']}\n"
            f"🎬 Режиссёр: {movie_info['Director']}\n"
            f"⭐️ Рейтинг IMDb: {movie_info['imdbRating']}\n"
            f"📖 Описание (ENG): {description}\n"
            f"📖 Описание (RUS): {translated_description}\n"
        )
        await message.answer_photo(photo=poster, caption=info)
    else:
        await message.answer("Фильм не найден. Попробуйте ещё раз.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
