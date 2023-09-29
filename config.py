from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = config("TOKEN")
bot =Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN_ID = 549937614
BOT_PIC = '/Users/macbook/PycharmProjects/Month3/media/bot_pic.jpeg'
ANIMATION_PIC = '/Users/macbook/PycharmProjects/Month3/media/Unknown.gif'
GROUP_ID = -4080196074
DESTINATION_DIR = "/Users/macbook/PycharmProjects/Month3/media"
