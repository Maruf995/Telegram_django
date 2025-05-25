from aiogram import Router, F
from aiogram.types import CallbackQuery
from asgiref.sync import sync_to_async
from product.models import Product
from users.models import User, CartItem

router = Router()

@router.callback_query(F.data.startswith("confirm_add_"))
async def add_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1])
    telegram_id = callback.from_user.id

    user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
    product = await sync_to_async(Product.objects.get)(id=product_id)

    try:
        cart_item = await sync_to_async(CartItem.objects.get)(user=user, product=product)
        cart_item.quantity += 1
        await sync_to_async(cart_item.save)()
    except CartItem.DoesNotExist:
        await sync_to_async(CartItem.objects.create)(user=user, product=product, quantity=1)

    await callback.message.answer(f"Товар {product.name} добавлен в корзину!")
    await callback.answer()
