from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import REQUIRED_CHANNELS
from keyboards.check import is_user_subscribed
from keyboards.main import main_menu

router = Router()

@router.callback_query(F.data == "check_subs")
async def check_subs(callback: CallbackQuery, bot):
    user_id = callback.from_user.id
    unsubscribed = []

    for channel_id in REQUIRED_CHANNELS:
        if not await is_user_subscribed(bot, user_id, channel_id):
            unsubscribed.append(channel_id)

    if unsubscribed:
        await callback.answer("Вы ещё не подписались на все каналы!", show_alert=True)
    else:
        await callback.message.answer("Спасибо за подписку! 🎉", reply_markup=main_menu())
        await callback.answer()
