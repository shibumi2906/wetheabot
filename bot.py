import logging
import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import requests
import config
from googletrans import Translator


async def main():
    bot = Bot(token=config.API_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()

    # Создаем папку для сохранения изображений, если ее нет
    if not os.path.exists('img'):
        os.makedirs('img')

    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я бот для прогноза погоды. Введите команду /help для получения списка команд.")

    @dp.message(Command("help"))
    async def send_help(message: types.Message):
        await message.reply(
            "Я могу отправить тебе прогноз погоды, сохранить фото, отправить голосовое сообщение и перевести текст на английский. Используйте команду /weather для получения прогноза погоды, отправьте фото для его сохранения, отправьте текст для его перевода.")

    @dp.message(Command("weather"))
    async def get_weather(message: types.Message):
        city = 'Ашкелон, Израиль'
        latitude = 31.6693
        longitude = 34.5715
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m'

        response = requests.get(url)
        data = response.json()

        if 'error' in data:
            await message.reply("Не удалось получить прогноз погоды. Попробуйте позже.")
        else:
            weather_description = data['hourly']['temperature_2m'][0]  # [0] чтобы получить текущую температуру
            await message.reply(f"Погода в {city}:\nТемпература: {weather_description}°C")

    @dp.message(F.photo)
    async def save_photo(message: types.Message):
        photo = message.photo[-1]
        file_path = await bot.download(photo, destination=f'img/{photo.file_id}.jpg')

        list_of_responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
        rand_answ = random.choice(list_of_responses)
        await message.answer(rand_answ)

    @dp.message(Command("voice"))
    async def send_voice(message: types.Message):
        voice_message = open("path_to_voice_message.ogg", 'rb')
        await bot.send_voice(message.chat.id, voice_message)
        voice_message.close()

    @dp.message(F.text)
    async def translate_text(message: types.Message):
        translator = Translator()
        translated = translator.translate(message.text, dest='en')
        await message.reply(translated.text)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
