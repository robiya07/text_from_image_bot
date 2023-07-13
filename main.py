import aiogram
import logging
import pytesseract
from PIL import Image
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

logging.basicConfig(level=logging.INFO)

bot = aiogram.Bot(token=config.get('TOKEN'))
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: aiogram.types.Message):
    await message.reply("Привет! Отправьте мне изображение с текстом.")


@dp.message_handler(content_types=aiogram.types.ContentTypes.PHOTO)
async def handle_image(message: aiogram.types.Message):
    photo_id = message.photo[-1].file_id
    file_info = await bot.get_file(photo_id)
    image_path = file_info.file_path
    file_extension = os.path.splitext(image_path)[1]
    file_name = f"{message.from_user.id}_{message.message_id}{file_extension}"
    file_path = os.path.join('photos', file_name)
    print(pytesseract.get_languages())
    await bot.download_file(image_path, file_path)

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang='eng')

    await message.reply(text)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
