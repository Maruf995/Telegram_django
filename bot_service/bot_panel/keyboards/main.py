from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="Корзина", callback_data="view_cart")],
            [InlineKeyboardButton(text="FAQ", callback_data="faq_start")]
        ]
    )
