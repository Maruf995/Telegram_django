# keyboards/cart.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from users.models import CartItem
from asgiref.sync import sync_to_async

async def cart_kb(user):
    cart_items = await sync_to_async(list)(CartItem.objects.filter(user=user))
    buttons = []

    for item in cart_items:
        buttons.append([
            InlineKeyboardButton(
                text=f"❌ {item.product.name} x{item.quantity}",
                callback_data=f"remove_{item.product.id}"
            )
        ])

    if cart_items:
        buttons.append([
            InlineKeyboardButton(text="✅ Оформить заказ", callback_data="make_order")
        ])
    else:
        buttons.append([InlineKeyboardButton(text="Корзина пуста", callback_data="empty_cart")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

