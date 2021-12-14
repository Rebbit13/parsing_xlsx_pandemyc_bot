import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, InputFile
from aiogram.utils import executor

from main import bot_parse

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level='INFO', filename="logs.log", format=LOG_FORMAT)
logger = logging.getLogger()

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)


@dispatcher.message_handler(content_types=["document"])
async def state(message: Message):
    if os.environ['IS_BUSY'] == "True":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Бот пока занят, попробуйте позже")
    elif os.environ['IS_BUSY'] == "False":
        os.environ['IS_BUSY'] = "True"
        await bot.send_message(chat_id=message.from_user.id,
                               text="В процессе, ожидайте")
        input_file_path = f'source/temp_file.xlsx'
        await message.document.download(destination_file=input_file_path)
        await asyncio.sleep(2)
        try:
            output_file_path = bot_parse(input_file_path)
        except Exception as error:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Что-то пошло не так\n{error}")
        else:
            file = InputFile(output_file_path)
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Готово!")
            await bot.send_document(chat_id=message.from_user.id,
                                    document=file)
        os.environ['IS_BUSY'] = "False"


async def send():
    file = InputFile("result.xlsx")
    await bot.send_message(chat_id=355117987,
                           text="Готово!")
    await bot.send_document(chat_id=355117987,
                            document=file,
                            disable_content_type_detection=True)


if __name__ == '__main__':
    os.environ['IS_BUSY'] = "False"
    executor.start_polling(dispatcher, skip_updates=True)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(send())
