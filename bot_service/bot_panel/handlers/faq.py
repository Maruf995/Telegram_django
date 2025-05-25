from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "faq_start")
async def faq_start_callback(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔍 Поиск FAQ в этом чате",
                switch_inline_query_current_chat="" 
            )
        ]
    ])
    await callback.message.answer(
        "Введите вопрос или нажмите кнопку для поиска по FAQ:",
        reply_markup=kb
    )
    await callback.answer()
