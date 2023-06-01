import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

from BlackWhite2Color import process_image


logging.basicConfig(level=logging.INFO)
load_dotenv()
# Telegram bot token (replace with your own)
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
        image = message.photo[-1].file_id
        file_path = await bot.get_file(image)
        downloaded_file = await bot.download_file(file_path.file_path)
        process_image(downloaded_file)

        await bot.send_photo(message.chat.id, photo=open('orig_after.png', 'rb'))

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)