from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from aiogram import Bot, F
from aiogram.fsm.context import FSMContext

from utils.add_new_user import add_new_user
from router import router, logger
from config import pay_token, data_base_path
from states import BuyQrs
from messages import text
from utils.manipulation_qrs_count import plus_qr
from keyboards import menu_keyboard
qr_count: int = 0

@router.message(Command(commands=["buy"]))
async def get_qrs_count(msg: Message, state: FSMContext):
    """
    Получение количества куаркодов которых хочет купить пользователь
    :param msg:
    :param state:
    :return:
    """
    logger.info(f"/buy {msg.from_user.username} получение количества желаемого количества qr кодов")
    add_new_user(data_base_path, username=msg.from_user.username)
    await state.set_state(BuyQrs.get_count)
    await msg.reply(text["get_buy_count"])


@router.message(BuyQrs.get_count)
async def payment(msg: Message, bot: Bot, state: FSMContext):
    """
    Отправка чека пользователю
    :param msg:
    :param bot:
    :param state:
    :return:
    """
    global qr_count
    logger.info(f"инициализация платежа количество qr кодов = {msg.text}")
    if msg.text.isdigit():
        await msg.bot.send_invoice(
            chat_id=msg.chat.id,
            title=f"{msg.text} qr code",
            description=f"покупка {msg.text} qr",
            provider_token=pay_token,
            payload=f"{msg.text} qr code",
            currency="UAH",
            prices=[
                LabeledPrice(
                    label="qr codes",
                    amount=3000 * int(msg.text),
                )
            ],
            max_tip_amount=10000,
            request_timeout=30
        )
        qr_count = int(msg.text)
        await state.clear()
    else:
        await msg.reply("Вы ввели не число")
        await state.clear()


@router.pre_checkout_query()
async def pre_check_out(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    """
    Одобрение покупки
    :param pre_checkout_query:
    :param bot:
    :return:
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    plus_qr(
        data_base_path=data_base_path,
        username=pre_checkout_query.from_user.username,
        count=qr_count
    )


@router.message(F.content_type == SuccessfulPayment)
async def successful_payment(msg: Message):
    """
    Уведомление пользователя об успешной покупке
    :param msg:
    :return:
    """
    await msg.reply("ok", reply_markup=menu_keyboard)
