from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from users.models import User, CartItem
import os
import pandas as pd
from aiogram.exceptions import TelegramBadRequest


router = Router()

def build_cart_keyboard(cart_items):
    keyboard = []
    for item in cart_items:
        keyboard.append([
            InlineKeyboardButton(
                text=f"Удалить {item.product.name}",
                callback_data=f"remove_from_cart_{item.product.id}"
            )
        ])
    if cart_items:
        keyboard.append([
            InlineKeyboardButton(
                text="Оформить заказ",
                callback_data="place_order"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.callback_query(F.data == "view_cart")
async def view_cart(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)

    cart_items = await sync_to_async(list)(CartItem.objects.filter(user=user).select_related('product'))

    if not cart_items:
        await callback.message.answer("Ваша корзина пуста.")
        await callback.answer()
        return

    message = "<b>Ваша корзина:</b>\n\n"
    for item in cart_items:
        message += f"{item.product.name} — {item.quantity} шт.\n"

    kb = build_cart_keyboard(cart_items)

    await callback.message.answer(message, parse_mode="HTML", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery):
    user = await sync_to_async(User.objects.get)(telegram_id=callback.from_user.id)

    message = (
        "<b>Проверьте свои данные:</b>\n"
        f"Имя: {user.first_name} {user.second_name}\n"
        f"Email: {user.email}\n"
        f"Телефон: {user.number}\n"
        f"Адрес: {user.address}"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить заказ", callback_data="confirm_order")]
        ]
    )

    await callback.message.answer(message, reply_markup=kb)
    await callback.answer()

ORDERS_FILE = "orders.xlsx"

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery):
    user = await sync_to_async(User.objects.get)(telegram_id=callback.from_user.id)
    cart_items = await sync_to_async(list)(user.cart_items.select_related("product").all())

    order_data = []
    for item in cart_items:
        order_data.append({
            "Telegram ID": user.telegram_id,
            "Имя": user.first_name,
            "Фамилия": user.second_name,
            "Email": user.email,
            "Телефон": user.number,
            "Адрес": user.address,
            "Название товара": item.product.name,
            "Количество": item.quantity,
        })

    current_order_df = pd.DataFrame(order_data)

    if os.path.exists(ORDERS_FILE):
        all_orders_df = pd.read_excel(ORDERS_FILE)
        all_orders_df = pd.concat([all_orders_df, current_order_df], ignore_index=True)
    else:
        all_orders_df = current_order_df

    all_orders_df.to_excel(ORDERS_FILE, index=False)

    await callback.message.answer("✅ Ваш заказ подтверждён!")
    await callback.answer()


@router.callback_query(F.data.startswith("remove_from_cart_"))
async def remove_from_cart(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
    
    product_id_str = callback.data.removeprefix("remove_from_cart_")
    try:
        product_id = int(product_id_str)
    except ValueError:
        await callback.answer("Ошибка: неверный ID товара.", show_alert=True)
        return

    cart_item = await sync_to_async(CartItem.objects.filter(user=user, product_id=product_id).first)()
    if cart_item:
        await sync_to_async(cart_item.delete)()
        await callback.answer("Товар удалён из корзины.")
    else:
        await callback.answer("Товар не найден в корзине.", show_alert=True)
        return

    cart_items = await sync_to_async(list)(CartItem.objects.filter(user=user).select_related('product'))
    if not cart_items:
        try:
            await callback.message.edit_text("🛒 Ваша корзина пуста.")
            await callback.message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                pass
            else:
                raise
    else:
        message = "<b>Ваша корзина:</b>\n\n"
        for item in cart_items:
            message += f"{item.product.name} — {item.quantity} шт.\n"
        kb = build_cart_keyboard(cart_items)
        try:
            await callback.message.edit_text(message, parse_mode="HTML", reply_markup=kb)
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                pass
            else:
                raise