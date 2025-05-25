# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import REQUIRED_CHANNELS
from keyboards.check import is_user_subscribed
from keyboards.main import main_menu

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message, bot):
    user_id = message.from_user.id
    unsubscribed = []

    for channel_id in REQUIRED_CHANNELS:
        if not await is_user_subscribed(bot, user_id, channel_id):
            unsubscribed.append(channel_id)

    if unsubscribed:
        buttons = [
            [InlineKeyboardButton(text="🔔 Перейти к подписке", url=f"https://t.me/c/{str(abs(chat_id))[4:]}")]
            for chat_id in unsubscribed
        ]
        buttons.append([InlineKeyboardButton(text="✅ Я подписался", callback_data="check_subs")])

        await message.answer(
            "Перед использованием бота, подпишитесь на следующие каналы:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
    else:
        await message.answer("Добро пожаловать в магазин!", reply_markup=main_menu())
