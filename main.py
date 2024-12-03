from aiogram import Dispatcher, executor
from config import BOT
from hadnlers import register_handlers

dp = Dispatcher(BOT)
register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)