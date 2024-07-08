from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile, URLInputFile
from messages import text
from states import MakeBasicQRCode
from router import router, logger

from keyboards import menu_keyboard
from config import data_base_path
from utils.mk_basic_qr import create_basic_qr
from utils.manipulation_qrs_count import minus_qr, get_qrs_count
from utils.add_new_user import add_new_user


@router.message(Command("CreateQR"))
async def get_data(msg: types.Message, state: FSMContext):
    """
    Инициализирует создание куаркода, после выполнения этой функции бот ожидает данные для шифрования в куар код
    :param msg:
    :param state:
    :return:
    """
    add_new_user(data_base_path, username=msg.from_user.username)
    logger.info(f"/basicQRcpde {msg.from_user.username} получение данных")
    qrs_count: int = get_qrs_count(
        data_base_path=data_base_path,
        username=msg.from_user.username)

    if qrs_count <= 0:
        logger.info(
            f"пользователю {msg.from_user.username} отказано в создании куаркода по тому что у него их не осталось")
        await msg.reply(text["basic_qr_no"].format(qrs_count), reply_markup=menu_keyboard)
        await state.clear()
    else:
        await state.set_state(MakeBasicQRCode.get_data)
        await msg.reply(text["basic_qr_get_data"].format(qrs_count), reply_markup=menu_keyboard)


@router.message(MakeBasicQRCode.get_data)
async def send_qr(msg: types.Message, state: FSMContext):
    """
    Тут происходит проверка на наличие куаркодов на аккаунет пользователя, создание и отправка
    :param msg:
    :param state:
    :return:
    """
    if get_qrs_count(
            data_base_path=data_base_path,
            username=msg.from_user.username) <= 0:
        logger.info(
            f"пользователю {msg.from_user.username} отказано в создании куаркода по тому что у него их не осталось")
        await msg.reply(text["basic_qr_no"], reply_markup=menu_keyboard)
        await state.clear()

    else:
        await msg.reply(text["creating"])
        data: str = msg.text
        path_png, path_tiff = create_basic_qr(data=data)



        if path_tiff == 0:
            await msg.reply(text["time_out"], reply_markup=menu_keyboard)
            await state.clear()
        else:
            minus_qr(
                data_base_path=data_base_path,
                username=msg.from_user.username,
                count=1
            )

            file_tiff = FSInputFile(path_tiff, filename="qr.tiff")
            file_png = FSInputFile(path=path_png)
            logger.info(f"/basicQRcode создан qr код с данными {msg.text} и отправлен {msg.from_user.username}")

            await msg.bot.send_photo(chat_id=msg.chat.id, photo=file_png)
            await msg.bot.send_document(chat_id=msg.chat.id, document=file_tiff)
            await msg.reply(
                text["send_qr"].format(
                    get_qrs_count(
                        data_base_path=data_base_path,
                        username=msg.from_user.username
                    )
                ),
                reply_markup=menu_keyboard
            )
            await state.clear()
