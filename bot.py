import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
import config


async def main():
    bot = Bot(token=config.API_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхук

    dp = Dispatcher()

    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Я бот для прогноза погоды. Введите команду /help для получения списка команд.")

    @dp.message(Command("help"))
    async def send_help(message: types.Message):
        await message.reply(
            "Я могу отправить тебе прогноз погоды. Введи команду /weather чтобы получить прогноз для города Ашкелон, Израиль.")

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

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
