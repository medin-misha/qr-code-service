from aiogram import types
from aiogram.filters import Command
from router import router, logger
from messages import text
from keyboards import menu_keyboard
from config import data_base_path
from utils.add_new_user import add_new_user


@router.message(Command(commands=['start']))
async def start(msg: types.Message):
    logger.info(f"/start пользователем {msg.from_user.username}")
    logger.info(f"аутентификация или регистрация пользователя в базе данных {msg.from_user.username}")

    add_new_user(data_base_path=data_base_path, username=msg.from_user.username)
    await msg.reply(text["start"], reply_markup=menu_keyboard)
