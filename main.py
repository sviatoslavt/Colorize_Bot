import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

from BlackWhite2Color import process_image


logging.basicConfig(level=logging.INFO)
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

help_message = """
👋 Вітаю! Я бот що розфарбує твоє чорно-біле фото!

Надішли мені фотографію і я розфарбую її!

Створено @svtashchuk
"""


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(help_message)

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
        image = message.photo[-1].file_id
        file_path = await bot.get_file(image)
        downloaded_file = await bot.download_file(file_path.file_path)
        message_id = await bot.send_message(message.chat.id, '⏳ Обробка зображення...')
        img = await process_image(downloaded_file)
        await bot.delete_message(message.chat.id, message_id.message_id)
        result = types.InputFile(img, filename='result.png')
        await bot.send_photo(message.chat.id, photo=result)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)